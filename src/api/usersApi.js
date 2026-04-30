import api from './axios'
export const getUsers = () => api.get('/users/')
export const createUser = (payload) => api.post('/users/', payload)
