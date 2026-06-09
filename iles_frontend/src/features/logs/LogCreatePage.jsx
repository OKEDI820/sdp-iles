import { useEffect, useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { createLog } from '../../api/logs'
import { fetchPlacements } from '../../api/placements'
import { errorMessage } from '../../api/client'
import { Button, Card, TextAreaField, TextField } from '../../components/ui'
import { useNotify } from '../../hooks/useNotify'
import { useAuthStore } from '../../auth/store'
import { isStudent } from '../../utils/constants'

export default function LogCreatePage() {
  const user = useAuthStore((s) => s.user)
  const notify = useNotify()
  const nav = useNavigate()
  const [placement, setPlacement] = useState(null)
  const [form, setForm] = useState({
    placement: '', week_number: 1, title: '', activities: '',
    challenges: '', lessons_learned: '', week_start: '', week_end: '',
  })
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    fetchPlacements().then((data) => {
      if (data.results?.length === 1) {
        const p = data.results[0]
        setPlacement(p)
        setForm((f) => ({ ...f, placement: p.id }))
      }
    })
  }, [])

  if (!isStudent(user)) return <Navigate to="/logs" replace />

  const validate = () => {
    const e = {}
    if (!form.placement) e.placement = 'Placement is required.'
    if (!form.title.trim()) e.title = 'Title is required.'
    if ((form.activities || '').trim().length < 10) e.activities = 'At least 10 characters.'
    if (!form.week_start) e.week_start = 'Week start is required.'
    if (!form.week_end) e.week_end = 'Week end is required.'
    if (form.week_start && form.week_end && form.week_start > form.week_end) {
      e.week_end = 'Cannot be before week start.'
    }
    if (!form.week_number || Number(form.week_number) < 1) {
      e.week_number = 'Must be a positive integer.'
    }
    return e
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
    if (errors[e.target.name]) setErrors({ ...errors, [e.target.name]: undefined })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const found = validate()
    setErrors(found)
    if (Object.keys(found).length) return
    setSubmitting(true)
    try {
      const created = await createLog({ ...form, week_number: Number(form.week_number) })
      notify.success('Draft log created.')
      nav(`/logs/${created.id}`)
    } catch (err) {
      const fields = err?.response?.data?.error?.fields
      if (fields) setErrors(fields)
      else notify.error(errorMessage(err))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Card title="New weekly log">
      <form onSubmit={handleSubmit}>
        {/* Display placement as read-only field */}
        <TextField
          label="Placement"
          value={placement?.company_name || 'Loading...'}
          readOnly
        />

        <div className="grid grid-2">
          <TextField label="Week number" name="week_number" type="number" min={1}
                     value={form.week_number} onChange={handleChange} error={errors.week_number} />
          <TextField label="Title" name="title" value={form.title}
                     onChange={handleChange} error={errors.title} />
          <TextField label="Week starts" name="week_start" type="date"
                     value={form.week_start} onChange={handleChange} error={errors.week_start} />
          <TextField label="Week ends" name="week_end" type="date"
                     value={form.week_end} onChange={handleChange} error={errors.week_end} />
        </div>
        <TextAreaField label="Activities (what you did)" name="activities" rows={5}
                       value={form.activities} onChange={handleChange} error={errors.activities} />
        <TextAreaField label="Challenges" name="challenges" rows={3}
                       value={form.challenges} onChange={handleChange} />
        <TextAreaField label="Lessons learned" name="lessons_learned" rows={3}
                       value={form.lessons_learned} onChange={handleChange} />
        <p className="muted" style={{ fontSize: '0.85rem' }}>
          Submission deadline is computed automatically from your placement's deadline-day setting.
        </p>
        <div className="row">
          <Button type="submit" loading={submitting}>Save draft</Button>
          <Button type="button" variant="secondary" onClick={() => nav('/logs')}>Cancel</Button>
        </div>
      </form>
    </Card>
  )
}