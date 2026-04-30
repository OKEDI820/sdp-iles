import { useState } from 'react'
import Button from '../../../components/common/Button'
import InputField from '../../../components/forms/InputField'
import TextAreaField from '../../../components/forms/TextAreaField'

const defaultForm = {
  student: '', placement: '', week_number: 1, title: '', activities: '', challenges: '', lessons_learned: '',
  date_from: '', date_to: '', submission_deadline: ''
}

export default function WeeklyLogForm({ onSubmit, initialData = defaultForm, students = [], placements = [], role = 'student' }) {
  const [form, setForm] = useState(initialData)
  const setField = (event) => setForm({ ...form, [event.target.name]: event.target.value })

  return (
    <form className="card" onSubmit={(event) => { event.preventDefault(); onSubmit(form); }}>
      <div className="grid-two">
        {role !== 'student' && <InputField label="Student ID" name="student" value={form.student} onChange={setField} />}
        <InputField label="Placement ID" name="placement" value={form.placement} onChange={setField} />
        <InputField label="Week Number" name="week_number" type="number" value={form.week_number} onChange={setField} />
        <InputField label="Title" name="title" value={form.title} onChange={setField} />
        <InputField label="Date From" name="date_from" type="date" value={form.date_from} onChange={setField} />
        <InputField label="Date To" name="date_to" type="date" value={form.date_to} onChange={setField} />
        <InputField label="Submission Deadline" name="submission_deadline" type="date" value={form.submission_deadline} onChange={setField} />
      </div>
      <TextAreaField label="Activities" name="activities" value={form.activities} onChange={setField} />
      <TextAreaField label="Challenges" name="challenges" value={form.challenges} onChange={setField} />
      <TextAreaField label="Lessons Learned" name="lessons_learned" value={form.lessons_learned} onChange={setField} />
      <Button>Save Log</Button>
    </form>
  )
}
