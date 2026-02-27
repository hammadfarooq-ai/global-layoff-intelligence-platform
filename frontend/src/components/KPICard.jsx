export default function KPICard({ title, value, subtext, icon }) {
  return (
    <div className="rounded-xl bg-slate-800/60 border border-slate-700/50 p-5 shadow-lg">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-slate-400 text-sm font-medium">{title}</p>
          <p className="mt-1 text-2xl font-display font-semibold text-white">
            {value}
          </p>
          {subtext && (
            <p className="mt-0.5 text-slate-500 text-sm">{subtext}</p>
          )}
        </div>
        {icon && (
          <div className="rounded-lg bg-slate-700/50 p-2 text-slate-400">
            {icon}
          </div>
        )}
      </div>
    </div>
  )
}
