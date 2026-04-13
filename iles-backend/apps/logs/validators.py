from django.utils import timezone
from rest_framework.exceptions import ValidationError

VALID_TRANSITIONS = {
    'draft': {'submitted'},
    'submitted': {'reviewed'},
    'reviewed': {'approved', 'draft'},
    'approved': set(),
}

def validate_transition(current_status, new_status):
    if new_status not in VALID_TRANSITIONS.get(current_status, set()):
        raise ValidationError({'detail': f'Invalid transition from {current_status} to {new_status}.'})

def validate_deadline(deadline):
    if timezone.localdate() > deadline:
        raise ValidationError({'detail': 'Submission deadline has passed.'})
