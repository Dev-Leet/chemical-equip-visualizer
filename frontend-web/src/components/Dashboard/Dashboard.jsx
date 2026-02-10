import { useState, useEffect } from 'react'
import Navbar from '../Common/Navbar'
import FileUpload from '../Upload/FileUpload'
import SummaryCards from './SummaryCards'
import DataTable from './DataTable'
import DoughnutChart from '../Visualization/DoughnutChart'
import BarChart from '../Visualization/BarChart'
import HistoryList from '../History/HistoryList'
import LoadingSpinner from '../Common/LoadingSpinner'
import { datasetAPI, summaryAPI } from '../../services/api'

export default function Dashboard() {
  const [currentDataset, setCurrentDataset] = useState(null)
  const [summary, setSummary] = useState(null)
  const [equipment, setEquipment] = useState([])
  const [loading, setLoading] = useState(false)
  const [refreshKey, setRefreshKey] = useState(0)

  const handleUploadSuccess = async (response) => {
    setRefreshKey(prev => prev + 1)
    await loadDataset(response.data.dataset_id)
  }

  const loadDataset = async (datasetId) => {
    setLoading(true)
    try {
      const [datasetRes, summaryRes] = await Promise.all([
        datasetAPI.get(datasetId),
        summaryAPI.get(datasetId)
      ])
      
      setCurrentDataset(datasetRes.data)
      setEquipment(datasetRes.data.equipment)
      setSummary(summaryRes.data)
    } catch (error) {
      console.error('Failed to load dataset:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSelectDataset = (datasetId) => {
    loadDataset(datasetId)
  }

  return (
    <div>
      <Navbar />
      
      <div className="container" style={{ paddingTop: '24px', paddingBottom: '24px' }}>
        <FileUpload onUploadSuccess={handleUploadSuccess} />

        {loading ? (
          <LoadingSpinner />
        ) : currentDataset ? (
          <>
            <SummaryCards summary={summary} />
            
            <div className="grid grid-2">
              <DataTable equipment={equipment} />
              <DoughnutChart data={summary?.type_distribution || []} />
            </div>

            <BarChart equipment={equipment} />
          </>
        ) : (
          <div className="card" style={{ textAlign: 'center', padding: '48px' }}>
            <p style={{ color: '#757575', fontSize: '16px' }}>Upload a CSV file to get started</p>
          </div>
        )}

        <HistoryList 
          onSelectDataset={handleSelectDataset} 
          refreshKey={refreshKey}
          currentDatasetId={currentDataset?.id}
        />
      </div>
    </div>
  )
}