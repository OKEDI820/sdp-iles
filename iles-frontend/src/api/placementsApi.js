import api from './axios'
export const getPlacements = () => api.get('/placements/')
export const createPlacement = (payload) => api.post('/placements/', payload)
export const updatePlacement = (id, payload) => api.patch(`/placements/${id}/`, payload)
