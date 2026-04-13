from decimal import Decimal

def calculate_total_score(technical_skills, communication, professionalism):
    return (
        Decimal(technical_skills) * Decimal('0.50') +
        Decimal(communication) * Decimal('0.20') +
        Decimal(professionalism) * Decimal('0.30')
    )
