export default function SummaryCards({ summary }) {
  if (!summary) return null

  const cards = [
    {
      label: 'Total Equipment',
      value: summary.statistics.total_count,
      icon: '📊'
    },
    {
      label: 'Avg Temperature',
      value: summary.statistics.averages.temperature ? `${summary.statistics.averages.temperature.toFixed(1)}°C` : 'N/A',
      icon: '🌡️'
    },
    {
      label: 'Avg Pressure',
      value: summary.statistics.averages.pressure ? `${summary.statistics.averages.pressure.toFixed(1)} bar` : 'N/A',
      icon: '⚡'
    },
    {
      label: 'Avg Flowrate',
      value: summary.statistics.averages.flowrate ? `${summary.statistics.averages.flowrate.toFixed(1)} L/m` : 'N/A',
      icon: '💨'
    }
  ]

  return (
    <div className="grid grid-4" style={{ marginBottom: '24px' }}>
      {cards.map((card, index) => (
        <div key={index} className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '48px', marginBottom: '8px' }}>{card.icon}</div>
          <div style={{ fontSize: '12px', color: '#757575', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '1px' }}>
            {card.label}
          </div>
          <div style={{ fontSize: '24px', fontWeight: '500', color: '#212121' }}>
            {card.value}
          </div>
        </div>
      ))}
    </div>
  )
}