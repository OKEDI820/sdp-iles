import { create } from 'zustand'

const savedUser = JSON.parse(localStorage.getItem('iles_user') || 'null')
const savedToken = localStorage.getItem('iles_access_token') || ''

export const useAuthStore = create((set) => ({
  user: savedUser,
  accessToken: savedToken,

  setSession: (token, user) => {
    localStorage.setItem('iles_access_token', token)
    localStorage.setItem('iles_user', JSON.stringify(user))
    set({ accessToken: token, user })
  },

  logout: () => {
    localStorage.removeItem('iles_access_token')
    localStorage.removeItem('iles_refresh_token')
    localStorage.removeItem('iles_user')
    set({ accessToken: '', user: null })
  },
}))