import { useState } from 'react'
import Button from '../../../components/common/Button'
import InputField from '../../../components/forms/InputField'
import TextAreaField from '../../../components/forms/TextAreaField'

const defaults = { weekly_log: '', technical_skills: 0, communication: 0, professionalism: 0, remarks: '' }

export default function EvaluationForm({ onSubmit }) {
  const [form, setForm] = useState(defaults)
  const onChange = (event) => setForm({ ...form, [event.target.name]: event.target.value })
  return (
    <form className="card" onSubmit={(event) => { event.preventDefault(); onSubmit(form) }}>
      <InputField label="Weekly Log ID" name="weekly_log" value={form.weekly_log} onChange={onChange} />
      <div className="grid-two">
        <InputField label="Technical Skills" name="technical_skills" type="number" value={form.technical_skills} onChange={onChange} />
        <InputField label="Communication" name="communication" type="number" value={form.communication} onChange={onChange} />
        <InputField label="Professionalism" name="professionalism" type="number" value={form.professionalism} onChange={onChange} />
      </div>
      <TextAreaField label="Remarks" name="remarks" value={form.remarks} onChange={onChange} />
      <Button>Save Evaluation</Button>
    </form>
  )
}
