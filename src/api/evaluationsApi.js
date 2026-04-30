import api from './axios'
export const getEvaluations = () => api.get('/evaluations/')
export const createEvaluation = => api.post('/evaluations/', payload)
export const updateEvaluation = (id, payload) => api.patch(`/evaluations/${id}/`, payload)
