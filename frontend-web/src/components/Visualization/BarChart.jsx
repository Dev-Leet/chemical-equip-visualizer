import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { Bar } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default function BarChart({ equipment }) {
  if (!equipment || equipment.length === 0) {
    return null
  }

  const chartData = {
    labels: equipment.slice(0, 10).map(item => item.equipment_name),
    datasets: [
      {
        label: 'Flowrate (L/m)',
        data: equipment.slice(0, 10).map(item => item.flowrate),
        backgroundColor: '#2196F3'
      },
      {
        label: 'Pressure (bar)',
        data: equipment.slice(0, 10).map(item => item.pressure),
        backgroundColor: '#4CAF50'
      },
      {
        label: 'Temperature (°C)',
        data: equipment.slice(0, 10).map(item => item.temperature),
        backgroundColor: '#FF9800'
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Parameter Comparison (First 10 Equipment)',
        font: { size: 16 }
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }

  return (
    <div className="card">
      <div style={{ height: '400px' }}>
        <Bar data={chartData} options={options} />
      </div>
    </div>
  )
}