import { Outlet, NavLink, useNavigate } from 'react-router-dom'

const nav = [
  { to: '/', label: 'Dashboard' },
  { to: '/trends', label: 'Trends' },
  { to: '/companies', label: 'Company Analysis' },
  { to: '/predict', label: 'Risk Prediction' },
]

export default function Layout() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-14">
            <h1 className="font-display font-semibold text-lg text-slate-100">
              Global Layoff Intelligence
            </h1>
            <nav className="flex items-center gap-1">
              {nav.map(({ to, label }) => (
                <NavLink
                  key={to}
                  to={to}
                  end={to === '/'}
                  className={({ isActive }) =>
                    `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-slate-700 text-white'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                    }`
                  }
                >
                  {label}
                </NavLink>
              ))}
              <button
                onClick={handleLogout}
                className="ml-4 px-3 py-2 text-sm text-slate-400 hover:text-rose-400 transition-colors"
              >
                Logout
              </button>
            </nav>
          </div>
        </div>
      </header>
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  )
}
