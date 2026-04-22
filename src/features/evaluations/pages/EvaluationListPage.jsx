import { useEffect, useState } from 'react'
import AppLayout from '../../../components/layout/AppLayout'
import PageHeader from '../../../components/layout/PageHeader'
import Card from '../../../components/common/Card'
import DataTable from '../../../components/tables/DataTable'
import { createEvaluation, getEvaluations } from '../../../api/evaluationsApi'
import EvaluationForm from '../components/EvaluationForm'
import CriteriaWeightCard from '../components/CriteriaWeightCard'
import ScoreSummary from '../components/ScoreSummary'

export default function EvaluationListPage() {
  const [evaluations, setEvaluations] = useState([])
  const load = async () => {
    const response = await getEvaluations()
    setEvaluations(response.data.results || response.data)
  }
  useEffect(() => { load().catch(console.error) }, [])

  return (
    <AppLayout>
      <PageHeader title="Evaluations" subtitle="Weighted scoring for weekly logs." />
      <div className="grid-two">
        <EvaluationForm onSubmit={async (payload) => { await createEvaluation(payload); load() }} />
        <div>
          <CriteriaWeightCard />
          <ScoreSummary evaluations={evaluations} />
        </div>
      </div>
      <Card title="Evaluation Records">
        <DataTable columns={[
          { key: 'week_number', label: 'Week' },
          { key: 'student_name', label: 'Student' },
          { key: 'evaluator_name', label: 'Evaluator' },
          { key: 'total_score', label: 'Total Score' },
        ]} rows={evaluations} />
      </Card>
    </AppLayout>
  )
}
