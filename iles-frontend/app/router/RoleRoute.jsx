import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function RoleRoute({ allowedRoles = [] }) {
  const user = useAuthStore((state) => state.user)
  if (!user) return <Navigate to="/login" replace />
  return allowedRoles.includes(user.role) ? <Outlet /> : <Navigate to="/" replace />
}
