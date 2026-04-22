import { useState } from 'react'
import Button from '../../../components/common/Button'
import InputField from '../../../components/forms/InputField'
import SelectField from '../../../components/forms/SelectField'

const defaults = { email: '', username: '', first_name: '', last_name: '', role: 'student', password: 'Pass1234!' }

export default function UserForm({ onSubmit }) {
  const [form, setForm] = useState(defaults)
  const onChange = (event) => setForm({ ...form, [event.target.name]: event.target.value })
  return <form className="card" onSubmit={(event) => { event.preventDefault(); onSubmit(form) }}><div className="grid-two"><InputField label="Email" name="email" value={form.email} onChange={onChange} /><InputField label="Username" name="username" value={form.username} onChange={onChange} /><InputField label="First Name" name="first_name" value={form.first_name} onChange={onChange} /><InputField label="Last Name" name="last_name" value={form.last_name} onChange={onChange} /><SelectField label="Role" name="role" value={form.role} onChange={onChange} options={[{value:'student',label:'Student'},{value:'supervisor',label:'Supervisor'},{value:'coordinator',label:'Coordinator'}]} /><InputField label="Password" name="password" value={form.password} onChange={onChange} /></div><Button>Create User</Button></form>
}
