import { useState } from 'react'

export default function DataTable({ equipment }) {
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10
  const totalPages = Math.ceil(equipment.length / itemsPerPage)

  const paginatedData = equipment.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  )

  return (
    <div className="card">
      <h3 style={{ marginBottom: '16px', fontSize: '20px', color: '#212121' }}>Equipment Data</h3>
      
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#F5F5F5' }}>
              <th style={{ padding: '12px', textAlign: 'left', fontWeight: '500', fontSize: '14px' }}>Name</th>
              <th style={{ padding: '12px', textAlign: 'left', fontWeight: '500', fontSize: '14px' }}>Type</th>
              <th style={{ padding: '12px', textAlign: 'right', fontWeight: '500', fontSize: '14px' }}>Flowrate</th>
              <th style={{ padding: '12px', textAlign: 'right', fontWeight: '500', fontSize: '14px' }}>Pressure</th>
              <th style={{ padding: '12px', textAlign: 'right', fontWeight: '500', fontSize: '14px' }}>Temp</th>
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((item, index) => (
              <tr key={item.id} style={{ backgroundColor: index % 2 === 0 ? 'white' : '#FAFAFA' }}>
                <td style={{ padding: '12px', fontSize: '14px' }}>{item.equipment_name}</td>
                <td style={{ padding: '12px', fontSize: '14px' }}>{item.equipment_type}</td>
                <td style={{ padding: '12px', textAlign: 'right', fontSize: '14px' }}>{item.flowrate}</td>
                <td style={{ padding: '12px', textAlign: 'right', fontSize: '14px' }}>{item.pressure}</td>
                <td style={{ padding: '12px', textAlign: 'right', fontSize: '14px' }}>{item.temperature}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginTop: '16px' }}>
          <button
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
            className="btn-secondary"
            style={{ padding: '8px 16px' }}
          >
            Previous
          </button>
          <span style={{ padding: '8px 16px', alignSelf: 'center' }}>
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            disabled={currentPage === totalPages}
            className="btn-secondary"
            style={{ padding: '8px 16px' }}
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}