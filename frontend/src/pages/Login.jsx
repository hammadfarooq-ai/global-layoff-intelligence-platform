import { useState } from 'react'
import { useNavigate, Navigate } from 'react-router-dom'
import { login } from '../api/client'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  if (localStorage.getItem('token')) {
    return <Navigate to="/" replace />
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const { access_token } = await login(username, password)
      localStorage.setItem('token', access_token)
      navigate('/', { replace: true })
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4">
      <div className="w-full max-w-sm rounded-2xl bg-slate-800/60 border border-slate-700/50 p-8 shadow-xl">
        <h1 className="font-display text-xl font-semibold text-white text-center mb-6">
          Global Layoff Intelligence
        </h1>
        <p className="text-slate-400 text-sm text-center mb-6">
          Sign in to access the dashboard
        </p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full rounded-lg bg-slate-900 border border-slate-600 px-3 py-2 text-white placeholder-slate-500 focus:ring-2 focus:ring-accent-blue focus:border-transparent"
              placeholder="admin"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg bg-slate-900 border border-slate-600 px-3 py-2 text-white placeholder-slate-500 focus:ring-2 focus:ring-accent-blue focus:border-transparent"
              placeholder="••••••••"
              required
            />
          </div>
          {error && (
            <p className="text-sm text-rose-400">{error}</p>
          )}
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-accent-blue hover:bg-blue-600 text-white font-medium py-2.5 transition-colors disabled:opacity-50"
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>
        <p className="mt-4 text-slate-500 text-xs text-center">
          Demo: admin / admin123
        </p>
      </div>
    </div>
  )
}
