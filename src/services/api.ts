import axios from "axios"

const API_BASE_URL = "/api"

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth API
export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post("/auth/login", { email, password })
    return response.data
  },

  verifyToken: async (token: string) => {
    const response = await api.get("/auth/verify", {
      headers: { Authorization: `Bearer ${token}` },
    })
    return response.data
  },
}

// Dashboard API
export const dashboardAPI = {
  getMetrics: async () => {
    const response = await api.get("/dashboard/metrics")
    return response.data
  },

  getRecentAlerts: async () => {
    const response = await api.get("/dashboard/alerts")
    return response.data
  },
}

// Weather API
export const weatherAPI = {
  getPredictions: async (location: string, timeRange: string) => {
    const response = await api.get(`/weather/predictions?location=${location}&range=${timeRange}`)
    return response.data
  },

  getRiskAssessment: async (location: string) => {
    const response = await api.get(`/weather/risk?location=${location}`)
    return response.data
  },

  getHistoricalData: async (location: string) => {
    const response = await api.get(`/weather/historical?location=${location}`)
    return response.data
  },
}

// Carbon API
export const carbonAPI = {
  getCompanies: async () => {
    const response = await api.get("/carbon/companies")
    return response.data
  },

  getCarbonData: async (companyId: string) => {
    const response = await api.get(`/carbon/data/${companyId}`)
    return response.data
  },

  getRecommendations: async (companyId: string) => {
    const response = await api.get(`/carbon/recommendations/${companyId}`)
    return response.data
  },

  uploadCarbonData: async (file: File) => {
    const formData = new FormData()
    formData.append("file", file)
    const response = await api.post("/carbon/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    return response.data
  },
}

// Urban Planning API
export const urbanAPI = {
  getCities: async () => {
    const response = await api.get("/urban/cities")
    return response.data
  },

  getCityData: async (cityId: string) => {
    const response = await api.get(`/urban/cities/${cityId}`)
    return response.data
  },

  getScenarios: async (cityId: string) => {
    const response = await api.get(`/urban/scenarios?city=${cityId}`)
    return response.data
  },

  getResilienceMetrics: async (cityId: string, scenarioId: string) => {
    const response = await api.get(`/urban/resilience?city=${cityId}&scenario=${scenarioId}`)
    return response.data
  },

  runSimulation: async (params: { cityId: string; scenarioId: string }) => {
    const response = await api.post("/urban/simulate", params)
    return response.data
  },
}
