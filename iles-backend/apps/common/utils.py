from django.db.models import Avg

def safe_average(queryset, field_name):
    return queryset.aggregate(value=Avg(field_name)).get('value') or 0
