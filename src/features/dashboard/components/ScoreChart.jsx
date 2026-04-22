import Card from '../../../components/common/Card'

export default function ScoreChart({ evaluations = [] }) {
  return (
    <Card title="Evaluation Scores">
      {evaluations.length ? evaluations.slice(0, 5).map((evaluation) => (
        <div key={evaluation.id} className="score-row">
          <span>Week {evaluation.week_number} - {evaluation.student_name}</span>
          <strong>{evaluation.total_score}</strong>
        </div>
      )) : <p className="muted">No evaluations yet.</p>}
    </Card>
  )
}
