ROLE_STUDENT = 'student'
ROLE_SUPERVISOR = 'supervisor'
ROLE_COORDINATOR = 'coordinator'

# Four-role labels per CSC 1202 Lecture 2.
ROLE_WORKPLACE_SUPERVISOR = 'workplace_supervisor'
ROLE_ACADEMIC_SUPERVISOR = 'academic_supervisor'
ROLE_ADMIN = 'admin'

ROLE_CHOICES = [
    (ROLE_STUDENT, 'Student Intern'),
    (ROLE_WORKPLACE_SUPERVISOR, 'Workplace Supervisor'),
    (ROLE_ACADEMIC_SUPERVISOR, 'Academic Supervisor'),
    (ROLE_ADMIN, 'Internship Administrator'),
    # Legacy roles kept for backward compatibility with existing data.
    (ROLE_SUPERVISOR, 'Supervisor (legacy)'),
    (ROLE_COORDINATOR, 'Coordinator (legacy)'),
]

LOG_DRAFT = 'draft'
LOG_SUBMITTED = 'submitted'
LOG_REVIEWED = 'reviewed'
LOG_APPROVED = 'approved'
LOG_REJECTED = 'rejected'

LOG_STATUS_CHOICES = [
    (LOG_DRAFT, 'Draft'),
    (LOG_SUBMITTED, 'Submitted'),
    (LOG_REVIEWED, 'Reviewed'),
    (LOG_APPROVED, 'Approved'),
    (LOG_REJECTED, 'Rejected'),
]
# Lookup for human-readable role names (used by serializers for `role_label`).
ROLE_LABELS = dict(ROLE_CHOICES)