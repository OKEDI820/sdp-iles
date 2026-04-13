ROLE_STUDENT = 'student'
ROLE_SUPERVISOR = 'supervisor'
ROLE_COORDINATOR = 'coordinator'
ROLE_CHOICES = [
    (ROLE_STUDENT, 'Student'),
    (ROLE_SUPERVISOR, 'Supervisor'),
    (ROLE_COORDINATOR, 'Coordinator'),
]

LOG_DRAFT = 'draft'
LOG_SUBMITTED = 'submitted'
LOG_REVIEWED = 'reviewed'
LOG_APPROVED = 'approved'
LOG_STATUS_CHOICES = [
    (LOG_DRAFT, 'Draft'),
    (LOG_SUBMITTED, 'Submitted'),
    (LOG_REVIEWED, 'Reviewed'),
    (LOG_APPROVED, 'Approved'),
]
