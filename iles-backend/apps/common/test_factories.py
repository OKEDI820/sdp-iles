"""Lightweight factory helpers for tests.

We avoid pulling in factory_boy — manual factories are clearer for a
class project of this size.
"""
from datetime import date, timedelta

from apps.common.choices import PlacementStatus, Role
from apps.placements.models import InternshipPlacement
from apps.users.models import User


def make_user(role: Role, *, email: str | None = None, **kwargs) -> User:
    email = email or f"{role.value}@test.example"
    defaults = {
        "username": role.value + str(User.objects.count()),
        "full_name": role.label,
        "role": role.value,
    }
    defaults.update(kwargs)
    user = User.objects.create_user(email=email, password="StrongPass123!", **defaults)
    return user


def make_placement(*, student=None, workplace=None, academic=None,
                  start=None, end=None, **kwargs) -> InternshipPlacement:
    student = student or make_user(Role.STUDENT, student_number="STD-001")
    workplace = workplace or make_user(
        Role.WORKPLACE_SUPERVISOR,
        email="workplace@test.example", staff_number="WS-001",
    )
    academic = academic or make_user(
        Role.ACADEMIC_SUPERVISOR,
        email="academic@test.example", staff_number="AS-001",
    )
    start = start or (date.today() - timedelta(days=14))
    end = end or (date.today() + timedelta(days=70))
    defaults = {
        "company_name": "Acme Internships Ltd.",
        "company_address": "Kampala",
        "status": PlacementStatus.ACTIVE,
    }
    defaults.update(kwargs)
    return InternshipPlacement.objects.create(
        student=student,
        workplace_supervisor=workplace,
        academic_supervisor=academic,
        start_date=start,
        end_date=end,
        **defaults,
    )
