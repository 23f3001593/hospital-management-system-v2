import { createStore } from "vuex"
import axios from "axios"
import { jwtDecode } from "jwt-decode";

let refreshTimeoutId = null

const store = createStore({
  state() {
    return {
      user: {role: null},
      accessToken: null,
      isAuthenticated: false
    }
  },
  mutations: {
    setUser(state, user) {
      state.user = user || { role: null }
    },
    setAccessToken(state, token) {
      state.accessToken = token
      state.isAuthenticated = !!token
    },
    logout(state) {
      state.user = {role: null}
      state.accessToken = null
      state.isAuthenticated = false
    }
  },
  actions: {
    async login({ commit, dispatch }, credentials) {
      try {
        const response = await axios.post("/auth/login", credentials)
        const { access_token, refresh_token, user } = response.data

        commit("setUser", { role: user.role })
        commit("setAccessToken", access_token)

        localStorage.setItem("refresh_token", refresh_token)
        localStorage.setItem("user_role", user.role)

        axios.defaults.headers.common["Authorization"] = `Bearer ${access_token}`

        dispatch("scheduleTokenRefresh", access_token)
        return true
      } catch (error) {
        console.error("Login failed:", error.response?.data || error.message)
        throw error
      }
    },

    scheduleTokenRefresh({ dispatch }, accessToken) {
      try {
        const { exp } = jwtDecode(accessToken)
        const expiresIn = exp * 1000 - Date.now()
        const refreshBefore = Math.max(expiresIn - 60 * 1000, 0)

        if (refreshTimeoutId) clearTimeout(refreshTimeoutId)

        refreshTimeoutId = setTimeout(() => {
          dispatch("refreshAccessToken")
        }, refreshBefore)
      } catch (err) {
        console.error("Failed to schedule token refresh:", err)
      }
    },

    async refreshAccessToken({ commit, dispatch }) {
        const refresh_token = localStorage.getItem("refresh_token");
        if (!refresh_token) return;

        try {
            const response = await axios.post("/auth/refresh", {}, {
                headers: {Authorization: `Bearer ${refresh_token}`}
            });
            const newAccessToken = response.data.access_token;
            commit("setAccessToken", newAccessToken)
            axios.defaults.headers.common["Authorization"] = `Bearer ${newAccessToken}`
            dispatch("scheduleTokenRefresh", newAccessToken)
        } catch (err) {
            console.error("Token refresh failed:", err.response?.data || err.message)
            dispatch("logout")
        }
    },

    async restore({ commit, dispatch }) {
        const refreshToken = localStorage.getItem("refresh_token")
        const savedRole = localStorage.getItem("user_role")
        if (savedRole) commit("setUser", { role: savedRole })
        if (!refreshToken) return

        try {
            await dispatch("refreshAccessToken")
        } catch (err) {
            console.warn("Session expired or invalid token:", err)
            localStorage.removeItem("refresh_token")
            localStorage.removeItem("user_role")
        }
    },

    logout({ commit }) {
      localStorage.removeItem("refresh_token")
      localStorage.removeItem("user_role")
      commit("logout")
      delete axios.defaults.headers.common["Authorization"]
      if (refreshTimeoutId) clearTimeout(refreshTimeoutId)
    }
  }
})

export default store