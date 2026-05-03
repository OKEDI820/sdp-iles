from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.common.choices import LogStatus, Role
from apps.common.test_factories import make_placement, make_user
from apps.evaluations import services
from apps.evaluations.scoring import (
    COMMUNICATION_WEIGHT,
    PROFESSIONALISM_WEIGHT,
    TECHNICAL_WEIGHT,
    calculate_total,
)
from apps.logs import services as log_services


class ScoringTests(TestCase):
    """Lecture 1 says T*0.4 + C*0.3 + P*0.3."""

    def test_weights_match_spec(self):
        self.assertEqual(TECHNICAL_WEIGHT, Decimal("0.40"))
        self.assertEqual(COMMUNICATION_WEIGHT, Decimal("0.30"))
        self.assertEqual(PROFESSIONALISM_WEIGHT, Decimal("0.30"))

    def test_weights_sum_to_one(self):
        self.assertEqual(
            TECHNICAL_WEIGHT + COMMUNICATION_WEIGHT + PROFESSIONALISM_WEIGHT,
            Decimal("1.00"),
        )

    def test_max_inputs_yield_max_score(self):
        self.assertEqual(calculate_total(100, 100, 100), Decimal("100.00"))

    def test_known_combination(self):
        # 80*0.4 + 60*0.3 + 70*0.3 = 32 + 18 + 21 = 71
        self.assertEqual(calculate_total(80, 60, 70), Decimal("71.00"))

    def test_zeros(self):
        self.assertEqual(calculate_total(0, 0, 0), Decimal("0.00"))

    def test_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            calculate_total(101, 50, 50)
        with self.assertRaises(ValueError):
            calculate_total(50, -1, 50)


class EvaluationServiceTests(TestCase):
    def setUp(self):
        self.placement = make_placement()
        self.student = self.placement.student
        self.workplace = self.placement.workplace_supervisor
        self.academic = self.placement.academic_supervisor
        self.admin = make_user(Role.ADMIN, email="adm@test.example", staff_number="A1")

    def _approved_log(self):
        log = log_services.create_draft_log(
            student=self.student, placement=self.placement, week_number=1,
            title="Test", activities="Long enough activity description here.",
            week_start=date.today() - timedelta(days=7),
            week_end=date.today() - timedelta(days=1),
        )
        log = log_services.submit_log(log, actor=self.student)
        log = log_services.review_log(log, actor=self.workplace)
        log = log_services.approve_log(log, actor=self.academic)
        return log

    def test_create_evaluation_happy_path(self):
        log = self._approved_log()
        ev = services.create_evaluation(
            weekly_log=log, evaluator=self.academic,
            technical_skills=80, communication=60, professionalism=70,
            remarks="Solid",
        )
        self.assertEqual(ev.total_score, Decimal("71.00"))

    def test_cannot_evaluate_unapproved_log(self):
        log = log_services.create_draft_log(
            student=self.student, placement=self.placement, week_number=2,
            title="Draft", activities="Long enough activity description here.",
            week_start=date.today() - timedelta(days=7),
            week_end=date.today() - timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            services.create_evaluation(
                weekly_log=log, evaluator=self.academic,
                technical_skills=80, communication=60, professionalism=70,
            )

    def test_workplace_supervisor_cannot_evaluate(self):
        log = self._approved_log()
        with self.assertRaises(PermissionDenied):
            services.create_evaluation(
                weekly_log=log, evaluator=self.workplace,
                technical_skills=80, communication=60, professionalism=70,
            )

    def test_only_one_evaluation_per_log(self):
        log = self._approved_log()
        services.create_evaluation(
            weekly_log=log, evaluator=self.academic,
            technical_skills=80, communication=60, professionalism=70,
        )
        with self.assertRaises(ValidationError):
            services.create_evaluation(
                weekly_log=log, evaluator=self.academic,
                technical_skills=90, communication=90, professionalism=90,
            )

    def test_admin_can_evaluate_anyone(self):
        log = self._approved_log()
        ev = services.create_evaluation(
            weekly_log=log, evaluator=self.admin,
            technical_skills=100, communication=100, professionalism=100,
        )
        self.assertEqual(ev.total_score, Decimal("100.00"))
