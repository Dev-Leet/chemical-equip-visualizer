import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'react-chartjs-2'

ChartJS.register(ArcElement, Tooltip, Legend)

export default function DoughnutChart({ data }) {
  if (!data || data.length === 0) {
    return <div className="card"><p>No data available</p></div>
  }

  const chartData = {
    labels: data.map(item => item.equipment_type),
    datasets: [{
      data: data.map(item => item.count),
      backgroundColor: [
        '#2196F3',
        '#4CAF50',
        '#FF9800',
        '#9C27B0',
        '#F44336',
        '#00BCD4'
      ],
      borderWidth: 2,
      borderColor: '#fff'
    }]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 15,
          font: { size: 12 }
        }
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const label = context.label || ''
            const value = context.parsed || 0
            const percentage = data[context.dataIndex]?.percentage || 0
            return `${label}: ${value} (${percentage.toFixed(1)}%)`
          }
        }
      }
    }
  }

  return (
    <div className="card">
      <h3 style={{ marginBottom: '16px', fontSize: '20px', color: '#212121' }}>Equipment Type Distribution</h3>
      <div style={{ height: '300px' }}>
        <Doughnut data={chartData} options={options} />
      </div>
    </div>
  )
}