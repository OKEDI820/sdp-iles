// Mirror of backend choices. Keep in sync with apps/common/choices.py.

export const ROLES = {
  STUDENT: 'student',
  WORKPLACE_SUPERVISOR: 'workplace_supervisor',
  ACADEMIC_SUPERVISOR: 'academic_supervisor',
  ADMIN: 'admin',
}

export const ROLE_LABELS = {
  student: 'Student Intern',
  workplace_supervisor: 'Workplace Supervisor',
  academic_supervisor: 'Academic Supervisor',
  admin: 'Internship Administrator',
}

export const SUPERVISOR_ROLES = [
  ROLES.WORKPLACE_SUPERVISOR,
  ROLES.ACADEMIC_SUPERVISOR,
  ROLES.ADMIN,
]

export const STATUSES = {
  DRAFT: 'draft',
  SUBMITTED: 'submitted',
  REVIEWED: 'reviewed',
  APPROVED: 'approved',
  REJECTED: 'rejected',
}

export const STATUS_LABELS = {
  draft: 'Draft',
  submitted: 'Submitted',
  reviewed: 'Reviewed',
  approved: 'Approved',
  rejected: 'Rejected',
}

// Permission helpers — keep them in one place.
export const isStudent = (u) => u?.role === ROLES.STUDENT
export const isAdmin = (u) => u?.role === ROLES.ADMIN
export const isSupervisor = (u) => SUPERVISOR_ROLES.includes(u?.role)
export const canApprove = (u) =>
  u?.role === ROLES.ACADEMIC_SUPERVISOR || u?.role === ROLES.ADMIN
export const canReview = (u) => SUPERVISOR_ROLES.includes(u?.role)

// What actions are visible on a log given (user, log)?
export function availableLogActions(user, log) {
  if (!user || !log) return []
  const actions = []
  const isOwner = user.id === log.student
  const status = log.status

  if (isStudent(user) && isOwner) {
    if (status === STATUSES.DRAFT || status === STATUSES.REJECTED) {
      actions.push('edit', 'submit')
    }
  }
  if (canReview(user) && status === STATUSES.SUBMITTED) {
    actions.push('review', 'reject')
  }
  if (canApprove(user) && status === STATUSES.REVIEWED) {
    actions.push('approve')
  }
  if (canReview(user) && status === STATUSES.REVIEWED) {
    actions.push('request-revision', 'reject')
  }
  return actions
}
