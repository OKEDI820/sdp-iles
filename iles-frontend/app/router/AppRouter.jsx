import { Routes, Route } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'
import RoleRoute from './RoleRoute'
import LoginPage from '../../features/auth/pages/LoginPage'
import DashboardPage from '../../features/dashboard/pages/DashboardPage'
import WeeklyLogListPage from '../../features/logs/pages/WeeklyLogListPage'
import PlacementListPage from '../../features/placements/pages/PlacementListPage'
import EvaluationListPage from '../../features/evaluations/pages/EvaluationListPage'
import UserManagementPage from '../../features/users/pages/UserManagementPage'

export default function AppRouter() {
  return (
    
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/logs" element={<WeeklyLogListPage />} />
        <Route path="/placements" element={<PlacementListPage />} />
        <Route path="/evaluations" element={<EvaluationListPage />} />
        <Route element={<RoleRoute allowedRoles={['coordinator']} />}>
          <Route path="/users" element={<UserManagementPage />} />
        </Route>
      </Route>
    </Routes>
  )
}
