import { useState } from 'react'
import Button from '../../../components/common/Button'
import TextAreaField from '../../../components/forms/TextAreaField'

export default function ReviewLogPanel({ onReview, onRequestRevision }) {
  const [feedback, setFeedback] = useState('')
  return <div className="card"><TextAreaField label="Feedback" value={feedback} onChange={(e) => setFeedback(e.target.value)} /><div className="actions"><Button onClick={() => onReview({ feedback })}>Mark Reviewed</Button><Button variant="secondary" onClick={() => onRequestRevision({ feedback })}>Request Revision</Button></div></div>
}
