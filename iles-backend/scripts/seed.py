"""Seed the database with demo data for ILES.

Creates:
  - 1 admin, 1 workplace supervisor, 1 academic supervisor, 1 student
  - 1 placement linking student to both supervisors
  - 3 evaluation criteria (40 / 30 / 30, matching the formula)
  - 4 weekly logs in different states so all dashboards have data:
      week 1 → approved (with evaluation)
      week 2 → reviewed (awaiting approval)
      week 3 → submitted (awaiting review)
      week 4 → draft

Usage:  python scripts/seed.py
"""
import os
import sys
from datetime import date, timedelta
from pathlib import Path

# Make `apps.*` importable when running directly.
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

import django  # noqa: E402

django.setup()

from apps.common.choices import LogStatus, PlacementStatus, Role  # noqa: E402
from apps.evaluations.models import Evaluation, EvaluationCriterion  # noqa: E402
from apps.evaluations.scoring import calculate_total  # noqa: E402
from apps.logs.models import WeeklyLog  # noqa: E402
from apps.logs.services import compute_deadline  # noqa: E402
from apps.placements.models import InternshipPlacement  # noqa: E402
from apps.users.models import User  # noqa: E402


PASSWORD = "Pass1234!"


def upsert_user(email, *, role, full_name, **extra):
    user, _ = User.objects.update_or_create(
        email=email,
        defaults={
            "username": email.split("@")[0],
            "role": role,
            "full_name": full_name,
            **extra,
        },
    )
    user.set_password(PASSWORD)
    user.save()
    return user


def main():
    admin = upsert_user(
        "admin@example.com",
        role=Role.ADMIN, full_name="Admin User",
        staff_number="ADM-001", department="Internship Office",
        is_staff=True, is_superuser=True,
    )
    workplace = upsert_user(
        "workplace@example.com",
        role=Role.WORKPLACE_SUPERVISOR, full_name="Wendy Workplace",
        staff_number="WS-001",
    )
    academic = upsert_user(
        "academic@example.com",
        role=Role.ACADEMIC_SUPERVISOR, full_name="Adam Academic",
        staff_number="AS-001", department="Computer Science",
    )
    student = upsert_user(
        "student@example.com",
        role=Role.STUDENT, full_name="Sam Student",
        student_number="STD-2026-001", department="Computer Science",
    )

    # Placement.
    today = date.today()
    placement, _ = InternshipPlacement.objects.update_or_create(
        student=student,
        defaults={
            "workplace_supervisor": workplace,
            "academic_supervisor": academic,
            "company_name": "Tech Hub Uganda",
            "company_address": "Plot 7, Kampala",
            "company_contact": "+256 700 000 000",
            "start_date": today - timedelta(days=28),
            "end_date": today + timedelta(days=60),
            "status": PlacementStatus.ACTIVE,
            "weekly_log_deadline_day": 4,  # Friday
        },
    )

    # Criteria — names + percentages match the formula in scoring.py.
    for name, pct, desc in [
        ("Technical Skills", 40,
         "Quality of engineering work, problem solving, code/output."),
        ("Communication", 30,
         "Clarity in writing, reporting, collaboration."),
        ("Professionalism", 30,
         "Punctuality, initiative, work ethic, conduct."),
    ]:
        EvaluationCriterion.objects.update_or_create(
            name=name,
            defaults={"weight_percent": pct, "description": desc, "is_active": True},
        )

    # Four logs covering every workflow state.
    sample_logs = [
        # week 1 — approved
        {
            "week_number": 1,
            "title": "Onboarding & environment setup",
            "activities": "Completed onboarding, set up the dev environment, learned the company's git workflow, paired with a senior engineer on bug triage.",
            "challenges": "Configuring Docker locally took longer than expected.",
            "lessons_learned": "How to read a CI pipeline configuration.",
            "week_offset": -28,
            "status": LogStatus.APPROVED,
        },
        # week 2 — reviewed (awaiting approval)
        {
            "week_number": 2,
            "title": "First feature ticket",
            "activities": "Picked up a small CRUD ticket on the customer-facing dashboard, wrote unit tests, and submitted a PR that was merged after review.",
            "challenges": "Understanding the existing test fixtures.",
            "lessons_learned": "Importance of small focused PRs.",
            "week_offset": -21,
            "status": LogStatus.REVIEWED,
        },
        # week 3 — submitted (awaiting review)
        {
            "week_number": 3,
            "title": "API rate-limiting investigation",
            "activities": "Investigated intermittent 429s from a third-party API, added retries and backoff, documented findings.",
            "challenges": "Reproducing the flakiness was hard.",
            "lessons_learned": "Always log structured request metadata.",
            "week_offset": -14,
            "status": LogStatus.SUBMITTED,
        },
        # week 4 — draft (in progress)
        {
            "week_number": 4,
            "title": "Database migrations refactor",
            "activities": "Started splitting a monolithic migration. Learning about squash and reversible operations.",
            "challenges": "Some migrations are not reversible.",
            "lessons_learned": "Plan migrations carefully.",
            "week_offset": -7,
            "status": LogStatus.DRAFT,
        },
    ]

    for spec in sample_logs:
        week_start = today + timedelta(days=spec["week_offset"])
        week_end = week_start + timedelta(days=4)
        deadline = compute_deadline(week_end, placement.weekly_log_deadline_day)

        log, created = WeeklyLog.objects.update_or_create(
            student=student,
            week_number=spec["week_number"],
            defaults={
                "placement": placement,
                "title": spec["title"],
                "activities": spec["activities"],
                "challenges": spec["challenges"],
                "lessons_learned": spec["lessons_learned"],
                "week_start": week_start,
                "week_end": week_end,
                "submission_deadline": deadline,
                "status": spec["status"],
            },
        )

        # Mark workflow timestamps based on status, so dashboards have realistic data.
        from django.utils import timezone
        now = timezone.now()
        updates = {}
        if spec["status"] in (LogStatus.SUBMITTED, LogStatus.REVIEWED, LogStatus.APPROVED):
            updates["submitted_at"] = now - timedelta(days=2)
        if spec["status"] in (LogStatus.REVIEWED, LogStatus.APPROVED):
            updates["reviewed_at"] = now - timedelta(days=1)
            updates["reviewed_by"] = workplace
            updates["review_feedback"] = "Solid effort. Add more reflection next time."
        if spec["status"] == LogStatus.APPROVED:
            updates["approved_at"] = now
            updates["approved_by"] = academic
            if updates:
                WeeklyLog.objects.filter(pk=log.pk).update(**updates)

    # Evaluation for the approved log (week 1).
    week1 = WeeklyLog.objects.get(student=student, week_number=1)
    Evaluation.objects.update_or_create(
        weekly_log=week1,
        defaults={
            "evaluator": academic,
            "technical_skills": 80,
            "communication": 75,
            "professionalism": 90,
            "total_score": calculate_total(80, 75, 90),
            "remarks": "Strong start to the placement.",
        },
    )

    print()
    print("Seed complete. Demo accounts (password is 'Pass1234!'):")
    print()
    print(f"  admin@example.com      Internship Administrator")
    print(f"  academic@example.com   Academic Supervisor")
    print(f"  workplace@example.com  Workplace Supervisor")
    print(f"  student@example.com    Student Intern")
    print()
    print("Sample data: 1 placement, 4 weekly logs (one per workflow state),")
    print("3 criteria (40/30/30), 1 evaluation.")


if __name__ == "__main__":
    main()
