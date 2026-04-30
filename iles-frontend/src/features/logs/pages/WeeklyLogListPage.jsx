import { useEffect, useState } from 'react'
import AppLayout from '../../../components/layout/AppLayout'
import PageHeader from '../../../components/layout/PageHeader'
import Card from '../../../components/common/Card'
import { getLogs, createLog, submitLog, reviewLog, approveLog, requestRevision } from '../../../api/logsApi'
import WeeklyLogForm from '../components/WeeklyLogForm'
import WeeklyLogTable from '../components/WeeklyLogTable'
import ReviewLogPanel from '../components/ReviewLogPanel'
import ApprovalActions from '../components/ApprovalActions'
import Button from '../../../components/common/Button'
import { useAuthStore } from '../../../app/store/authStore'

export default function WeeklyLogListPage() {
  const [logs, setLogs] = useState([])
  const [selectedLog, setSelectedLog] = useState(null)
  const user = useAuthStore((state) => state.user)

  const loadLogs = async () => {
    const response = await getLogs()
    setLogs(response.data.results || response.data)
  }

  useEffect(() => { loadLogs().catch(console.error) }, [])

  const handleCreate = async (payload) => {
    await createLog(payload)
    loadLogs()
  }

  const handleAction = async (action) => {
    if (!selectedLog) return
    await action(selectedLog.id)
    loadLogs()
  }

  return (
    <AppLayout>
      <PageHeader title="Weekly Logs" subtitle="Create, submit, review, and approve internship logs." />
      <div className="grid-two logs-grid">
        <WeeklyLogForm onSubmit={handleCreate} role={user?.role} />
        <Card title="Logs Table">
          <WeeklyLogTable rows={logs} />
          <div className="actions wrap">
            {logs.map((log) => <Button key={log.id} variant={selectedLog?.id === log.id ? 'secondary' : 'primary'} onClick={() => setSelectedLog(log)}>Select Week {log.week_number}</Button>)}
          </div>
        </Card>
      </div>
      {selectedLog ? <div className="grid-two">
        <Card title={`Selected Log: Week ${selectedLog.week_number}`}>
          <p><strong>{selectedLog.title}</strong></p>
          <p>{selectedLog.activities}</p>
          <p className="muted">Current status: {selectedLog.status}</p>
          {user?.role === 'student' && selectedLog.status === 'draft' ? <Button onClick={() => handleAction(submitLog)}>Submit Selected Log</Button> : null}
          {(user?.role === 'supervisor' || user?.role === 'coordinator') && selectedLog.status === 'reviewed' ? <ApprovalActions onApprove={() => handleAction(approveLog)} /> : null}
        </Card>
        {(user?.role === 'supervisor' || user?.role === 'coordinator') && selectedLog.status !== 'approved' ? (
          <ReviewLogPanel
            onReview={async (payload) => { await reviewLog(selectedLog.id, payload); loadLogs() }}
            onRequestRevision={async (payload) => { await requestRevision(selectedLog.id, payload); loadLogs() }}
          />
        ) : null}
      </div> : null}
    </AppLayout>
  )
}
