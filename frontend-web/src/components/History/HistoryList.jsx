import { useState, useEffect } from 'react'
import { datasetAPI, reportAPI } from '../../services/api'

export default function HistoryList({ onSelectDataset, refreshKey, currentDatasetId }) {
  const [datasets, setDatasets] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDatasets()
  }, [refreshKey])

  const loadDatasets = async () => {
    try {
      const response = await datasetAPI.list({ active_only: true })
      setDatasets(response.data.results)
    } catch (error) {
      console.error('Failed to load datasets:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id, e) => {
    e.stopPropagation()
    if (window.confirm('Are you sure you want to delete this dataset?')) {
      try {
        await datasetAPI.delete(id)
        loadDatasets()
      } catch (error) {
        alert('Failed to delete dataset')
      }
    }
  }

  const handleDownloadPDF = async (id, filename, e) => {
    e.stopPropagation()
    try {
      const response = await reportAPI.getPDF(id)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${filename.replace('.csv', '')}_report.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      alert('Failed to generate PDF')
    }
  }

  if (loading) return <div className="card">Loading history...</div>

  return (
    <div className="card">
      <h3 style={{ marginBottom: '16px', fontSize: '20px', color: '#212121' }}>Recent Uploads</h3>
      
      {datasets.length === 0 ? (
        <p style={{ color: '#757575' }}>No datasets uploaded yet</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {datasets.map(dataset => (
            <div
              key={dataset.id}
              onClick={() => onSelectDataset(dataset.id)}
              style={{
                padding: '16px',
                border: dataset.id === currentDatasetId ? '2px solid #1976D2' : '1px solid #E0E0E0',
                borderRadius: '8px',
                cursor: 'pointer',
                backgroundColor: dataset.id === currentDatasetId ? '#E3F2FD' : 'white',
                transition: 'all 0.3s'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: '500', marginBottom: '4px' }}>📄 {dataset.filename}</div>
                  <div style={{ fontSize: '12px', color: '#757575' }}>
                    {dataset.row_count} items • {new Date(dataset.upload_date).toLocaleDateString()}
                  </div>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button
                    onClick={(e) => handleDownloadPDF(dataset.id, dataset.filename, e)}
                    className="btn-secondary"
                    style={{ padding: '8px 16px' }}
                  >
                    PDF
                  </button>
                  <button
                    onClick={(e) => handleDelete(dataset.id, e)}
                    style={{
                      padding: '8px 16px',
                      backgroundColor: 'transparent',
                      color: '#C62828',
                      border: '1px solid #C62828',
                      borderRadius: '4px'
                    }}
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}