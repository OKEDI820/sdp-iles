import api from './axios'
export const getEvaluations = () => api.get('/evaluations/')
export const createEvaluation = (payload) => api.post('/evaluations/', payload)
export const updateEvaluation = (id, payload) => api.patch(`/evaluations/${id}/`, payload)
