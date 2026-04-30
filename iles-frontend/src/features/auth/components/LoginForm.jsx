import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getCurrentUserWithToken, loginRequest } from '../../../api/authApi'
import { useAuthStore } from '../../../app/store/authStore'
import InputField from '../../../components/forms/InputField'
import FormError from '../../../components/forms/FormError'
import Button from '../../../components/common/Button'

export default function LoginForm() {
  const [form, setForm] = useState({
    email: 'student@example.com',
    password: 'Pass1234!',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const setSession = useAuthStore((state) => state.setSession)
  const navigate = useNavigate()

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value })
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')

    try {
      const loginResponse = await loginRequest({
        email: form.email,
        password: form.password,
      })

      const access = loginResponse.data.access
      const refresh = loginResponse.data.refresh

      if (!access) {
        throw new Error('No access token returned from backend')
      }

      localStorage.setItem('iles_access_token', access)
      localStorage.setItem('iles_refresh_token', refresh || '')

      const meResponse = await getCurrentUserWithToken(access)

      setSession(access, meResponse.data)
      navigate('/')
    } catch (err) {
      console.log('LOGIN ERROR:', err.response?.data || err.message)
      setError(
        err.response?.data?.detail ||
          err.message ||
          'Login failed. Check backend and credentials.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="card login-card" onSubmit={handleSubmit}>
      <h2>Sign in</h2>
      <p className="muted">Use one of the seeded accounts to test the system fast.</p>

      <InputField
        label="Email"
        name="email"
        value={form.email}
        onChange={handleChange}
      />

      <InputField
        label="Password"
        name="password"
        type="password"
        value={form.password}
        onChange={handleChange}
      />

      <FormError message={error} />

      <Button disabled={loading}>
        {loading ? 'Signing in...' : 'Login'}
      </Button>

      <div className="hint-box">
        <small>student@example.com / Pass1234!</small>
        <small>supervisor@example.com / Pass1234!</small>
        <small>coordinator@example.com / Pass1234!</small>
      </div>
    </form>
  )
}
