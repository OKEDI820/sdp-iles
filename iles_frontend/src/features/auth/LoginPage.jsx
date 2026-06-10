import { useState } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { fetchMe, login } from '../../api/auth'
import { errorMessage } from '../../api/client'
import { Button, Card, TextField } from '../../components/ui'
import { selectIsAuthenticated, useAuthStore } from '../../auth/store'

export default function LoginPage() {
  const authed     = useAuthStore(selectIsAuthenticated)
  const setSession = useAuthStore((s) => s.setSession)
  const nav        = useNavigate()
  const loc        = useLocation()
  const from       = loc.state?.from || '/'

  const [form, setForm]     = useState({ email: 'student@example.com', password: 'Pass1234!' })
  const [error, setError]   = useState('')
  const [loading, setLoading] = useState(false)

  if (authed) return <Navigate to={from} replace />

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (!form.email || !form.password) {
      setError('Email and password are required.')
      return
    }
    setLoading(true)
    try {
      const tokens = await login(form)
      setSession({ user: null, accessToken: tokens.access, refreshToken: tokens.refresh })
      const me = await fetchMe()
      setSession({ user: me, accessToken: tokens.access, refreshToken: tokens.refresh })
      nav(from, { replace: true })
    } catch (err) {
      setError(errorMessage(err, 'Login failed.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-shell">
      <div className="login-card">
        <Card title="Sign in to ILES">
          <p className="muted" style={{ marginBottom: '1.5rem', fontSize: '0.875rem' }}>
            Internship Log &amp; Evaluation System
          </p>
          <form onSubmit={handleSubmit}>
            {error && <div className="alert">{error}</div>}
            <TextField
              label="Email address" name="email" type="email" autoComplete="username"
              value={form.email} onChange={handleChange}
            />
            <TextField
              label="Password" name="password" type="password" autoComplete="current-password"
              value={form.password} onChange={handleChange}
            />
            <Button type="submit" loading={loading}>Sign in</Button>
          </form>
        </Card>
      </div>
    </div>
  )
}
