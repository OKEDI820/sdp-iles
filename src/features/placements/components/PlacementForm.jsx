import { useState } from 'react'
import Button from '../../../components/common/Button'
import InputField from '../../../components/forms/InputField'

const defaults = { student: '', company_name: '', company_address: '', supervisor_name: '', supervisor_email: '', start_date: '', end_date: '', status: 'active' }

export default function PlacementForm({ onSubmit }) {
  const [form, setForm] = useState(defaults)
  const onChange = (event) => setForm({ ...form, [event.target.name]: event.target.value })
  return (
    <form className="card" onSubmit={(event) => { event.preventDefault(); onSubmit(form) }}>
      <div className="grid-two">
        <InputField label="Student ID" name="student" value={form.student} onChange={onChange} />
        <InputField label="Company Name" name="company_name" value={form.company_name} onChange={onChange} />
        <InputField label="Company Address" name="company_address" value={form.company_address} onChange={onChange} />
        <InputField label="Supervisor Name" name="supervisor_name" value={form.supervisor_name} onChange={onChange} />
        <InputField label="Supervisor Email" name="supervisor_email" value={form.supervisor_email} onChange={onChange} />
        <InputField label="Start Date" name="start_date" type="date" value={form.start_date} onChange={onChange} />
        <InputField label="End Date" name="end_date" type="date" value={form.end_date} onChange={onChange} />
      </div>
      <Button>Create Placement</Button>
    </form>
  )
}
