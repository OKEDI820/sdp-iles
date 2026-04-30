import DataTable from '../../../components/tables/DataTable'
import StatusBadge from '../../../components/tables/StatusBadge'

export default function WeeklyLogTable({ rows = [] }) {
  const columns = [
    { key: 'week_number', label: 'Week' },
    { key: 'title', label: 'Title' },
    { key: 'student_name', label: 'Student' },
    { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
  ]
  return <DataTable columns={columns} rows={rows} />
}
