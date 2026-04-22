import { useAuthStore } from '../../app/store/authStore'

export default function Navbar() {
  const { user, logout } = useAuthStore()
  return (
    <div className="navbar">
      <div>
        <strong>Internship Logging & Evaluation System</strong>
        <p className="muted">Real workflow project for coursework defense</p>
      </div>
      <div className="navbar-right">
        <span>{user?.full_name} ({user?.role})</span>
        <button className="btn btn-secondary" onClick={logout}>Logout</button>
      </div>
    </div>
  )
}
