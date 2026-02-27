import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Trends from './pages/Trends'
import CompanyAnalysis from './pages/CompanyAnalysis'
import RiskPrediction from './pages/RiskPrediction'
import Login from './pages/Login'

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token')
  if (!token) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="trends" element={<Trends />} />
        <Route path="companies" element={<CompanyAnalysis />} />
        <Route path="predict" element={<RiskPrediction />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
