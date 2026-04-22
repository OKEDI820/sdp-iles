import Card from '../../../components/common/Card'
import StatusBadge from '../../../components/tables/StatusBadge'

export default function RecentLogs({ logs = [] }) {
  return (
    <Card title="Recent Weekly Logs">
      {logs.length ? logs.slice(0, 5).map((log) => <div key={log.id} className="list-item"><div><strong>Week {log.week_number}: {log.title}</strong><p className="muted">{log.student_name || 'My log'}</p></div><StatusBadge status={log.status} /></div>) : <p className="muted">No logs yet.</p>}
    </Card>
  )
}
