import axios from 'axios'
import { useAuthStore } from '../auth/store'

/**
 * Single axios instance used for all API calls.
 *
 * - Attaches the JWT to every request.
 * - On 401, transparently tries to refresh and retry the original request.
 * - On refresh failure, clears the session so the router redirects to login.
 */
export const api = axios.create({
  baseURL: https://mukisa-api.tagooledavid.com/api/v1,
  headers: { 'Content-Type': 'application/json' },
})

// --- Request: attach JWT ---
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// --- Response: 401 → refresh + retry ---
let refreshing = null

api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config
    if (
      error.response?.status === 401 &&
      !original._retried &&
      original.url !== '/auth/refresh/' &&
      original.url !== '/auth/login/'
    ) {
      original._retried = true
      try {
        const newToken = await refreshAccessToken()
        original.headers.Authorization = `Bearer ${newToken}`
        return api(original)
      } catch (e) {
        useAuthStore.getState().clear()
      }
    }
    return Promise.reject(error)
  },
)

async function refreshAccessToken() {
  // Coalesce concurrent refreshes.
  if (refreshing) return refreshing
  const { refreshToken, setAccessToken } = useAuthStore.getState()
  if (!refreshToken) throw new Error('no-refresh-token')
  refreshing = axios
    .post(`${API_BASE_URL}/auth/refresh/`, { refresh: refreshToken })
    .then((res) => {
      setAccessToken(res.data.access)
      return res.data.access
    })
    .finally(() => {
      refreshing = null
    })
  return refreshing
}

/** Extracts a user-facing error message from an axios error. */
export function errorMessage(err, fallback = 'Something went wrong.') {
  const data = err?.response?.data
  if (typeof data?.error?.detail === 'string') return data.error.detail
  if (typeof data?.detail === 'string') return data.detail
  return err?.message || fallback
}
