import Card from '../../../components/common/Card'

export default function SummaryCards({ summary }) {
  const items = [
    ['Total Logs', summary.total_logs],
    ['Submitted', summary.submitted_logs],
    ['Reviewed', summary.reviewed_logs],
    ['Approved', summary.approved_logs],
    ['Evaluations', summary.total_evaluations],
    ['Average Score', Number(summary.average_score || 0).toFixed(2)],
  ]
  return <div className="stats-grid">{items.map(([label, value]) => <Card key={label}><p className="muted">{label}</p><h2>{value}</h2></Card>)}</div>
}
