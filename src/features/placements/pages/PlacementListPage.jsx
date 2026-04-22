import { useEffect, useState } from 'react'
import AppLayout from '../../../components/layout/AppLayout'
import PageHeader from '../../../components/layout/PageHeader'
import Card from '../../../components/common/Card'
import DataTable from '../../../components/tables/DataTable'
import { createPlacement, getPlacements } from '../../../api/placementsApi'
import PlacementForm from '../components/PlacementForm'

export default function PlacementListPage() {
  const [placements, setPlacements] = useState([])
  const load = async () => {
    const response = await getPlacements()
    setPlacements(response.data.results || response.data)
  }
  useEffect(() => { load().catch(console.error) }, [])

  return (
    <AppLayout>
      <PageHeader title="Placements" subtitle="Manage internship placement records." />
      <div className="grid-two">
        <PlacementForm onSubmit={async (payload) => { await createPlacement(payload); load() }} />
        <Card title="Placement Records">
          <DataTable
            columns={[
              { key: 'student_name', label: 'Student' },
              { key: 'company_name', label: 'Company' },
              { key: 'supervisor_name', label: 'Supervisor' },
              { key: 'status', label: 'Status' },
            ]}
            rows={placements}
          />
        </Card>
      </div>
    </AppLayout>
  )
}
