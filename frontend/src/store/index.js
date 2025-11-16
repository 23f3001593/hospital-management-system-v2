import { createStore } from "vuex"
import axios from "axios"
import { jwtDecode } from "jwt-decode";

let refreshTimeoutId = null

const store = createStore({
    state() {
        return {
            user: {id: null, role: null, fullname: null},
            accessToken: null,
            isAuthenticated: false
        }
    },
    mutations: {
        setUser(state, user) {
            state.user = user || {id: null, role: null, fullname: null}
        },
        setAccessToken(state, token) {
            state.accessToken = token
            state.isAuthenticated = !!token
        },
        logout(state) {
            state.user = {id: null, role: null, fullname: null}
            state.accessToken = null
            state.isAuthenticated = false
        }
    },
    actions: {
        async login({ commit, dispatch }, credentials) {
            const response = await axios.post("/auth/login", credentials)
            const { access_token, refresh_token, user } = response.data
            commit("setUser", { id: user.id, role: user.role, fullname: user.full_name })
            commit("setAccessToken", access_token)
            localStorage.setItem("refresh_token", refresh_token)
            localStorage.setItem("user_id", user.id)
            localStorage.setItem("user_role", user.role)
            localStorage.setItem("user_fullname", user.full_name)
            axios.defaults.headers.common["Authorization"] = `Bearer ${access_token}`
            dispatch("scheduleTokenRefresh", access_token)
            return true
        },
        scheduleTokenRefresh({ dispatch }, accessToken) {
            const { exp } = jwtDecode(accessToken)
            const expiresIn = exp * 1000 - Date.now()
            const refreshBefore = Math.max(expiresIn - 60 * 1000, 0)
            if (refreshTimeoutId) clearTimeout(refreshTimeoutId)
            refreshTimeoutId = setTimeout(() => {dispatch("refreshAccessToken")}, refreshBefore)
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
                dispatch("logout")
            }
        },
        async restore({ commit, dispatch }) {
            const refreshToken = localStorage.getItem("refresh_token")
            const savedId = localStorage.getItem("user_id")
            const savedRole = localStorage.getItem("user_role")
            const savedFullname = localStorage.getItem("user_fullname")
            if (savedId && savedRole && savedFullname) commit("setUser", { id:savedId, role: savedRole, fullname: savedFullname })
            if (!refreshToken) return
            try {
                await dispatch("refreshAccessToken")
            } catch (err) {
                localStorage.removeItem("refresh_token")
                localStorage.removeItem("user_id")
                localStorage.removeItem("user_role")
                localStorage.removeItem("user_fullname")
            }
        },
        logout({ commit }) {
            localStorage.removeItem("refresh_token")
            localStorage.removeItem("user_id")
            localStorage.removeItem("user_role")
            localStorage.removeItem("user_fullname")
            commit("logout")
            delete axios.defaults.headers.common["Authorization"]
            if (refreshTimeoutId) {
                clearTimeout(refreshTimeoutId)
                refreshTimeoutId = null
            }
        }
    }
})

export default store