"""Tests for the weekly log workflow.

Coverage:
  - state transition rules (Lecture 2)
  - deadline enforcement (Lecture 1)
  - service-layer authorisation (Lecture 4)
  - signal-driven email + audit (Lecture 7)
"""
from datetime import date, timedelta

from django.core import mail
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.audit.models import AuditEntry
from apps.common.choices import LogStatus, Role
from apps.common.test_factories import make_placement, make_user
from apps.logs import services
from apps.logs.models import WeeklyLog
from apps.logs.validators import (
    VALID_TRANSITIONS,
    assert_deadline_not_passed,
    assert_transition,
)


class StateMachineTests(TestCase):
    """Lecture 2: only the listed transitions are valid."""

    def test_dict_covers_every_state(self):
        for s in LogStatus:
            self.assertIn(s.value, VALID_TRANSITIONS)

    def test_legal_transitions(self):
        legal = [
            (LogStatus.DRAFT, LogStatus.SUBMITTED),
            (LogStatus.SUBMITTED, LogStatus.REVIEWED),
            (LogStatus.SUBMITTED, LogStatus.REJECTED),
            (LogStatus.REVIEWED, LogStatus.APPROVED),
            (LogStatus.REVIEWED, LogStatus.DRAFT),
            (LogStatus.REVIEWED, LogStatus.REJECTED),
            (LogStatus.REJECTED, LogStatus.DRAFT),
        ]
        for old, new in legal:
            with self.subTest(transition=(old, new)):
                assert_transition(old, new)  # should not raise

    def test_illegal_transitions_raise(self):
        illegal = [
            (LogStatus.DRAFT, LogStatus.APPROVED),
            (LogStatus.DRAFT, LogStatus.REVIEWED),
            (LogStatus.APPROVED, LogStatus.DRAFT),
            (LogStatus.APPROVED, LogStatus.SUBMITTED),
        ]
        for old, new in illegal:
            with self.subTest(transition=(old, new)):
                with self.assertRaises(ValidationError):
                    assert_transition(old, new)


class DeadlineTests(TestCase):
    def test_today_is_allowed(self):
        assert_deadline_not_passed(date.today())

    def test_past_is_blocked(self):
        with self.assertRaises(ValidationError):
            assert_deadline_not_passed(date.today() - timedelta(days=1))


class ServiceLayerTests(TestCase):
    def setUp(self):
        self.placement = make_placement()
        self.student = self.placement.student
        self.workplace = self.placement.workplace_supervisor
        self.academic = self.placement.academic_supervisor
        self.admin = make_user(Role.ADMIN, email="admin@test.example", staff_number="A1")

    def _create_log(self, **overrides):
        defaults = {
            "student": self.student,
            "placement": self.placement,
            "week_number": 1,
            "title": "Week 1",
            "activities": "Onboarding and setup activities completed.",
            "week_start": date.today() - timedelta(days=7),
            "week_end": date.today() - timedelta(days=1),
        }
        defaults.update(overrides)
        return services.create_draft_log(**defaults)

    # --- happy path ---

    def test_full_lifecycle(self):
        log = self._create_log()
        log = services.submit_log(log, actor=self.student)
        log = services.review_log(log, actor=self.workplace, feedback="Good")
        log = services.approve_log(log, actor=self.academic)

        self.assertEqual(log.status, LogStatus.APPROVED)
        self.assertEqual(log.reviewed_by, self.workplace)
        self.assertEqual(log.approved_by, self.academic)

    # --- authorisation rules ---

    def test_only_owner_can_submit(self):
        other_student = make_user(Role.STUDENT, email="other@test.example",
                                   student_number="STD-2")
        log = self._create_log()
        with self.assertRaises(PermissionDenied):
            services.submit_log(log, actor=other_student)

    def test_only_assigned_workplace_supervisor_can_review(self):
        rogue = make_user(
            Role.WORKPLACE_SUPERVISOR,
            email="rogue@test.example", staff_number="WS-X",
        )
        log = services.submit_log(self._create_log(), actor=self.student)
        with self.assertRaises(PermissionDenied):
            services.review_log(log, actor=rogue)

    def test_only_academic_or_admin_can_approve(self):
        log = services.review_log(
            services.submit_log(self._create_log(), actor=self.student),
            actor=self.workplace,
        )
        with self.assertRaises(PermissionDenied):
            services.approve_log(log, actor=self.workplace)

    def test_admin_can_approve_anyone(self):
        log = services.review_log(
            services.submit_log(self._create_log(), actor=self.student),
            actor=self.workplace,
        )
        log = services.approve_log(log, actor=self.admin)
        self.assertEqual(log.status, LogStatus.APPROVED)

    # --- rejection & revision ---

    def test_rejection_path(self):
        log = services.submit_log(self._create_log(), actor=self.student)
        log = services.reject_log(log, actor=self.workplace, reason="Insufficient detail.")
        self.assertEqual(log.status, LogStatus.REJECTED)
        self.assertEqual(log.rejection_reason, "Insufficient detail.")

    def test_rejected_log_can_be_returned_to_draft(self):
        log = services.reject_log(
            services.submit_log(self._create_log(), actor=self.student),
            actor=self.workplace, reason="Try again.",
        )
        # Manually move to draft (would happen via update endpoint;
        # we go direct here to test the state allows it).
        from apps.logs.validators import assert_transition
        assert_transition(LogStatus.REJECTED, LogStatus.DRAFT)

    def test_revision_request_returns_log_to_draft(self):
        log = services.review_log(
            services.submit_log(self._create_log(), actor=self.student),
            actor=self.workplace,
        )
        log = services.request_revision(
            log, actor=self.workplace, message="Please expand on Tuesday."
        )
        self.assertEqual(log.status, LogStatus.DRAFT)

    # --- editability ---

    def test_approved_log_is_immutable(self):
        log = services.approve_log(
            services.review_log(
                services.submit_log(self._create_log(), actor=self.student),
                actor=self.workplace,
            ),
            actor=self.academic,
        )
        with self.assertRaises(ValidationError):
            services.update_draft(log, actor=self.student, title="Tampered")

    def test_draft_can_be_edited(self):
        log = self._create_log()
        log = services.update_draft(
            log, actor=self.student,
            title="New title", activities="More than ten chars of new content.",
        )
        self.assertEqual(log.title, "New title")


class DeadlineEnforcementTests(TestCase):
    def test_cannot_submit_past_deadline(self):
        placement = make_placement()
        log = WeeklyLog.objects.create(
            student=placement.student,
            placement=placement,
            week_number=1,
            title="Late one",
            activities="Some valid description here.",
            week_start=date.today() - timedelta(days=14),
            week_end=date.today() - timedelta(days=8),
            submission_deadline=date.today() - timedelta(days=1),  # past
            status=LogStatus.DRAFT,
        )
        with self.assertRaises(ValidationError):
            services.submit_log(log, actor=placement.student)


class SignalTests(TestCase):
    """Lecture 7: status changes fire emails AND audit entries."""

    def setUp(self):
        self.placement = make_placement()
        self.student = self.placement.student
        self.workplace = self.placement.workplace_supervisor
        self.academic = self.placement.academic_supervisor
        # Suppress 'log created' email noise from setUp.
        mail.outbox = []
        AuditEntry.objects.all().delete()

    def _make_log(self):
        return services.create_draft_log(
            student=self.student, placement=self.placement, week_number=1,
            title="Test", activities="A long enough description.",
            week_start=date.today() - timedelta(days=7),
            week_end=date.today() - timedelta(days=1),
        )

    def test_submit_emails_workplace_supervisor(self):
        mail.outbox = []
        services.submit_log(self._make_log(), actor=self.student)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.workplace.email, mail.outbox[0].to)

    def test_review_emails_student_and_academic(self):
        log = services.submit_log(self._make_log(), actor=self.student)
        mail.outbox = []
        services.review_log(log, actor=self.workplace, feedback="Decent.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.student.email, mail.outbox[0].to)
        self.assertIn(self.academic.email, mail.outbox[0].to)

    def test_approval_emails_only_student(self):
        log = services.review_log(
            services.submit_log(self._make_log(), actor=self.student),
            actor=self.workplace,
        )
        mail.outbox = []
        services.approve_log(log, actor=self.academic)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.student.email])

    def test_audit_entries_recorded_for_each_transition(self):
        log = self._make_log()
        AuditEntry.objects.all().delete()
        services.submit_log(log, actor=self.student)
        services.review_log(log, actor=self.workplace)
        services.approve_log(log, actor=self.academic)

        actions = list(
            AuditEntry.objects.filter(target_type="WeeklyLog")
            .order_by("created_at").values_list("action", flat=True)
        )
        self.assertEqual(actions, [
            "log.status.submitted",
            "log.status.reviewed",
            "log.status.approved",
        ])
