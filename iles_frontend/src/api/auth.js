import axios from 'axios'
    // Import the new constant
import { api, API_BASE_URL } from './client'
   
    export async function login({ email, password }) {
      // Use the constant instead of a hardcoded string
      const res = await axios.post(`${API_BASE_URL}/auth/login/`, { email, password })
      return res.data 
    }

export async function fetchMe() {
  const res = await api.get('/auth/me/')
  return res.data
}

export async function changePassword({ oldPassword, newPassword }) {
  const res = await api.post('/auth/change-password/', {
    old_password: oldPassword,
    new_password: newPassword,
  })
  return res.data
}
