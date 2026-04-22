import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000/api'

export const loginRequest = (payload) =>
  axios.post(`${API_BASE}/auth/login/`, payload, {
    headers: {
      'Content-Type': 'application/json',
    },
  })

export const getCurrentUserWithToken = (token) =>
  axios.get(`${API_BASE}/auth/me/`, {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  })

export const getStoredAccessToken = () => localStorage.getItem('iles_access_token') || ''