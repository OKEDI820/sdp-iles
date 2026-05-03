import { create } from 'zustand'
import { persist } from 'zustand/middleware'

/**
 * Auth state.
 *
 * Tokens live in localStorage so a refresh keeps the user logged in.
 * On every 401 the axios interceptor (api/client.js) attempts a refresh;
 * if that fails, it calls `clear()` to log the user out.
 */
export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      setSession: ({ user, accessToken, refreshToken }) =>
        set({ user, accessToken, refreshToken }),
      setAccessToken: (accessToken) => set({ accessToken }),
      setUser: (user) => set({ user }),
      clear: () => set({ user: null, accessToken: null, refreshToken: null }),
    }),
    { name: 'iles-auth' },
  ),
)

export const selectIsAuthenticated = (s) => Boolean(s.accessToken && s.user)
