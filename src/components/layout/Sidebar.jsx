import { NavLink } from 'react-router-dom'
import { useAuthStore } from '../../app/store/authStore'

export default function Sidebar() {
  const user = useAuthStore((state) => state.user)
  const links = [
    { to: '/', label: 'Dashboard' },
    { to: '/logs', label: 'Weekly Logs' },
    { to: '/placements', label: 'Placements' },
    { to: '/evaluations', label: 'Evaluations' },
  ]
  if (user?.role === 'coordinator') links.push({ to: '/users', label: 'Users' })
  return (
    <aside className="sidebar">
      {links.map((link) => <NavLink key={link.to} to={link.to}>{link.label}</NavLink>)}
    </aside>
  )
}
