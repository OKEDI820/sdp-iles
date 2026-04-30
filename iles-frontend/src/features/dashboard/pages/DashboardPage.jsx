import { useEffect, useState } from 'react'
import AppLayout from '../../../components/layout/AppLayout'
import PageHeader from '../../../components/layout/PageHeader'
import Loader from '../../../components/common/Loader'
import { getDashboardSummary } from '../../../api/dashboardApi'
import { getLogs } from '../../../api/logsApi'
import { getEvaluations } from '../../../api/evaluationsApi'
import SummaryCards from '../components/SummaryCards'
import RecentLogs from '../components/RecentLogs'
import ScoreChart from '../components/ScoreChart'

export default function DashboardPage() {
  const [summary, setSummary] = useState(null)
  const [logs, setLogs] = useState([])
  const [evaluations, setEvaluations] = useState([])

  useEffect(() => {
    async function loadData() {
      const [summaryResponse, logsResponse, evaluationsResponse] = await Promise.all([
        getDashboardSummary(),
        getLogs(),
        getEvaluations(),
      ])
      setSummary(summaryResponse.data)
      setLogs(logsResponse.data.results || logsResponse.data)
      setEvaluations(evaluationsResponse.data.results || evaluationsResponse.data)
    }
    loadData().catch(console.error)
  }, [])

  return (
    <AppLayout>
      <PageHeader title="Dashboard" subtitle="Track workflow, deadlines, and evaluation progress." />
      {!summary ? <Loader /> : <>
        <SummaryCards summary={summary} />
        <div className="grid-two">
          <RecentLogs logs={logs} />
          <ScoreChart evaluations={evaluations} />
        </div>
      </>}
    </AppLayout>
  )
}
