import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchDashboard } from '../../api/users'
import { errorMessage } from '../../api/client'
import { Card, Stat, StatusBadge } from '../../components/ui'
import { useAuthStore } from '../../auth/store'
import { ROLE_LABELS, STATUS_LABELS } from '../../utils/constants'
import { formatDate, formatDateTime } from '../../utils/date'

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user)
  const [data, setData]   = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchDashboard().then(setData).catch((e) => setError(errorMessage(e)))
  }, [])

  if (error) return <div className="alert">{error}</div>
  if (!data)  return <Card><p className="muted">Loading…</p></Card>

  return (
    <div className="grid" style={{ gap: '1.25rem' }}>
      {/* Welcome banner */}
      <div className="welcome-banner">
        <h2>Welcome back, {user?.full_name?.split(' ')[0] || 'there'} 👋</h2>
        <p>{ROLE_LABELS[user?.role]} dashboard · {new Date().toLocaleDateString('en-GB', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
      </div>

      {data.role === 'student'               && <StudentBoard   data={data} />}
      {data.role === 'workplace_supervisor'  && <WorkplaceBoard data={data} />}
      {data.role === 'academic_supervisor'   && <AcademicBoard  data={data} />}
      {data.role === 'admin'                 && <AdminBoard     data={data} />}
    </div>
  )
}

// ── Student ────────────────────────────────────────────────────────────────

function StudentBoard({ data }) {
  return (
    <>
      <div className="grid grid-3">
        <Stat label="Total logs"       value={data.total_logs} />
        <Stat label="Approved"         value={data.log_counts.approved} />
        <Stat label="Awaiting review"  value={data.log_counts.submitted} />
        <Stat label="Drafts"           value={data.log_counts.draft} />
        <Stat label="Average score"    value={data.average_score?.toFixed(1) ?? '—'} />
        <Stat label="Placement"        value={data.has_placement ? 'Active' : 'None'} />
      </div>
      <Card title="Recent logs" actions={<Link to="/logs">View all →</Link>}>
        {data.recent_logs.length === 0
          ? <p className="muted">You have no logs yet. Create your first one.</p>
          : data.recent_logs.map((l) => (
              <div key={l.id} className="log-row">
                <Link to={`/logs/${l.id}`}>Week {l.week_number} — {l.title}</Link>
                <StatusBadge status={l.status} />
              </div>
            ))
        }
      </Card>
    </>
  )
}

// ── Workplace supervisor ───────────────────────────────────────────────────

function WorkplaceBoard({ data }) {
  return (
    <>
      <div className="grid grid-3">
        <Stat label="Students supervised" value={data.students_supervised} />
        <Stat label="Awaiting review"     value={data.awaiting_review} />
        <Stat label="Reviewed"            value={data.log_counts.reviewed} />
        <Stat label="Approved"            value={data.log_counts.approved} />
      </div>
      <Card title="Recent submissions awaiting review" actions={<Link to="/logs">All logs →</Link>}>
        {data.recent_submissions.length === 0
          ? <p className="muted">No logs need your review right now.</p>
          : data.recent_submissions.map((l) => (
              <div key={l.id} className="log-row">
                <Link to={`/logs/${l.id}`}>Week {l.week_number} — {l.student__full_name}</Link>
                <span className="muted" style={{ fontSize: '0.82rem' }}>{formatDateTime(l.submitted_at)}</span>
              </div>
            ))
        }
      </Card>
    </>
  )
}

// ── Academic supervisor ────────────────────────────────────────────────────

function AcademicBoard({ data }) {
  return (
    <>
      <div className="grid grid-3">
        <Stat label="Students supervised" value={data.students_supervised} />
        <Stat label="Awaiting approval"   value={data.awaiting_approval} />
        <Stat label="Evaluations given"   value={data.evaluations_given} />
        <Stat label="Avg score"           value={data.average_score_given?.toFixed(1) ?? '—'} />
      </div>
      <Card title="Logs awaiting approval" actions={<Link to="/logs">All logs →</Link>}>
        {data.to_approve.length === 0
          ? <p className="muted">All caught up.</p>
          : data.to_approve.map((l) => (
              <div key={l.id} className="log-row">
                <Link to={`/logs/${l.id}`}>Week {l.week_number} — {l.student__full_name}</Link>
                <span className="muted" style={{ fontSize: '0.82rem' }}>reviewed {formatDateTime(l.reviewed_at)}</span>
              </div>
            ))
        }
      </Card>
    </>
  )
}

// ── Admin ──────────────────────────────────────────────────────────────────

function AdminBoard({ data }) {
  return (
    <>
      <div className="grid grid-3">
        {Object.entries(data.user_counts).map(([role, n]) => (
          <Stat key={role} label={`${ROLE_LABELS[role] || role}s`} value={n} />
        ))}
      </div>
      <div className="grid grid-3">
        <Stat label="Active placements"   value={data.active_placements} />
        <Stat label="Total placements"    value={data.total_placements} />
        <Stat label="Average score"       value={data.average_score?.toFixed(1) ?? '—'} />
        <Stat label="Overdue submissions" value={data.overdue_submissions} />
      </div>
      <Card title="Log status breakdown">
        <div className="grid grid-3">
          {Object.entries(data.log_counts).map(([status, n]) => (
            <div key={status} className="row between" style={{ padding: '0.5rem 0.75rem', background: 'var(--surface-2)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-light)' }}>
              <StatusBadge status={status} />
              <strong style={{ fontSize: '1.1rem', fontWeight: 800 }}>{n}</strong>
            </div>
          ))}
        </div>
      </Card>
    </>
  )
}
