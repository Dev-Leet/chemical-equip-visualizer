import { useState, useRef } from 'react'
import { datasetAPI } from '../../services/api'

export default function FileUpload({ onUploadSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState('')
  const fileInputRef = useRef()

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      if (!file.name.endsWith('.csv')) {
        setError('Only CSV files are allowed')
        return
      }
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB')
        return
      }
      setSelectedFile(file)
      setError('')
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setUploading(true)
    setError('')
    setProgress(0)

    try {
      const response = await datasetAPI.upload(selectedFile, (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        setProgress(percentCompleted)
      })

      onUploadSuccess(response)
      setSelectedFile(null)
      if (fileInputRef.current) fileInputRef.current.value = ''
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.')
    } finally {
      setUploading(false)
      setProgress(0)
    }
  }

  return (
    <div className="card">
      <h2 style={{ fontSize: '20px', marginBottom: '16px', color: '#212121' }}>Upload Dataset</h2>
      
      <div style={{
        border: '2px dashed #E0E0E0',
        borderRadius: '8px',
        padding: '32px',
        textAlign: 'center',
        backgroundColor: '#FAFAFA'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '16px' }}>📁</div>
        <p style={{ marginBottom: '16px', color: '#757575' }}>
          {selectedFile ? selectedFile.name : 'Select a CSV file to upload'}
        </p>
        
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
          <button
            onClick={() => fileInputRef.current?.click()}
            className="btn-secondary"
            disabled={uploading}
          >
            Browse Files
          </button>
          
          {selectedFile && (
            <button
              onClick={handleUpload}
              className="btn-primary"
              disabled={uploading}
            >
              {uploading ? `Uploading... ${progress}%` : 'Upload'}
            </button>
          )}
        </div>

        {uploading && (
          <div style={{ marginTop: '16px' }}>
            <div style={{ 
              height: '8px', 
              backgroundColor: '#E0E0E0', 
              borderRadius: '4px', 
              overflow: 'hidden' 
            }}>
              <div style={{ 
                height: '100%', 
                width: `${progress}%`, 
                backgroundColor: '#1976D2',
                transition: 'width 0.3s'
              }} />
            </div>
          </div>
        )}

        {error && (
          <div className="error-message" style={{ marginTop: '16px' }}>{error}</div>
        )}
      </div>
    </div>
  )
}