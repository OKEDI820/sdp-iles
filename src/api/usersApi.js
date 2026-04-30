import api from './axios'
export const getUsers = () => api.get('/users/')
export const createUser =  => api.post('/users/', payload)
