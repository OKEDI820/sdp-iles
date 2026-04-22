import { useEffect, useState } from 'react'
import AppLayout from '../../../components/layout/AppLayout'
import PageHeader from '../../../components/layout/PageHeader'
import Card from '../../../components/common/Card'
import DataTable from '../../../components/tables/DataTable'
import { createUser, getUsers } from '../../../api/usersApi'
import UserForm from '../components/UserForm'

export default function UserManagementPage() {
  const [users, setUsers] = useState([])
  const load = async () => {
    const response = await getUsers()
    setUsers(response.data.results || response.data)
  }
  useEffect(() => { load().catch(console.error) }, [])
  return <AppLayout><PageHeader title="User Management" subtitle="Coordinator-only area for managing roles." /><div className="grid-two"><UserForm onSubmit={async (payload) => { await createUser(payload); load() }} /><Card title="Users"><DataTable columns={[{key:'id',label:'ID'},{key:'full_name',label:'Name'},{key:'email',label:'Email'},{key:'role',label:'Role'}]} rows={users} /></Card></div></AppLayout>
}
