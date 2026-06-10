import axios from 'axios'
import { api } from './client'

export async function login({ email, password }) {
  // Login uses bare axios (no interceptors) since we have no token yet.
  const res = await axios.post('/api/v1/auth/login/', { email, password })
  return res.data  // { access, refresh }
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
