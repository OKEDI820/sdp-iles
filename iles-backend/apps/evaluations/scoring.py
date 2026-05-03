"""Weighted scoring (CSC 1202 Lecture 1).

Final Score = T*0.4 + C*0.3 + P*0.3   with T, C, P each in [0, 100].

The weights are exposed as named Decimals so:
  - tests can assert they sum to 1.00
  - the frontend can read them via the API and stay in sync
"""
from decimal import Decimal


TECHNICAL_WEIGHT = Decimal("0.40")
COMMUNICATION_WEIGHT = Decimal("0.30")
PROFESSIONALISM_WEIGHT = Decimal("0.30")

WEIGHTS = {
    "technical_skills": TECHNICAL_WEIGHT,
    "communication": COMMUNICATION_WEIGHT,
    "professionalism": PROFESSIONALISM_WEIGHT,
}

assert sum(WEIGHTS.values()) == Decimal("1.00"), "weights must sum to 1.00"

MAX_SCORE = Decimal("100")


def calculate_total(technical: int, communication: int, professionalism: int) -> Decimal:
    """Returns the final weighted score as a Decimal in [0, 100]."""
    for label, value in (
        ("technical", technical),
        ("communication", communication),
        ("professionalism", professionalism),
    ):
        if not (0 <= value <= 100):
            raise ValueError(f"{label} must be between 0 and 100, got {value!r}")
    return (
        Decimal(technical) * TECHNICAL_WEIGHT
        + Decimal(communication) * COMMUNICATION_WEIGHT
        + Decimal(professionalism) * PROFESSIONALISM_WEIGHT
    )
