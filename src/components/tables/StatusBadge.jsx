import Badge from '../common/Badge'


export default function StatusBadge({ status }) {
  const tone = status === 'approved' ? 'success' : status === 'submitted' ? 'warning' : status === 'reviewed' ? 'info' : 'default'
  return <Badge tone={tone}>{status}</Badge>
}
