import api from './axios'
export const getLogs = () => api.get('/logs/')
export const createLog = (payload) => api.post('/logs/', payload)
export const updateLog = (id, payload) => api.patch(`/logs/${id}/`, payload)
export const submitLog = (id) => api.post(`/logs/${id}/submit/`)
export const reviewLog = (id, payload) => api.post(`/logs/${id}/review/`, payload)
export const approveLog = (id) => api.post(`/logs/${id}/approve/`)
export const requestRevision = (id, payload) => api.post(`/logs/${id}/request-revision/`, payload)
