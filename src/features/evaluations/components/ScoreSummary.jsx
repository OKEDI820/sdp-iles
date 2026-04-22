import Card from '../../../components/common/Card'
export default function ScoreSummary({ evaluations = [] }) {
  return <Card title="Score Summary">{evaluations.map((item) => <div key={item.id} className="score-row"><span>Week {item.week_number}</span><strong>{item.total_score}</strong></div>)}</Card>
}
