import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { selectIsAuthenticated, useAuthStore } from '../auth/store'

export function ProtectedRoute() {
  const authed = useAuthStore(selectIsAuthenticated)
  const loc = useLocation()
  if (!authed) return <Navigate to="/login" replace state={{ from: loc.pathname }} />
  return <Outlet />
}

export function RoleGate({ allow = [] }) {
  const user = useAuthStore((s) => s.user)
  if (!user) return <Navigate to="/login" replace />
  if (!allow.includes(user.role)) return <Navigate to="/" replace />
  return <Outlet />
}
