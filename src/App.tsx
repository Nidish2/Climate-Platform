import { Routes, Route } from "react-router-dom"
import { AuthProvider } from "./contexts/AuthContext"
import Layout from "./components/Layout"
import Dashboard from "./pages/Dashboard"
import WeatherPrediction from "./pages/WeatherPrediction"
import CarbonFootprint from "./pages/CarbonFootprint"
import UrbanPlanning from "./pages/UrbanPlanning"
import Login from "./pages/Login"
import ProtectedRoute from "./components/ProtectedRoute"

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Layout />}>
          <Route
            index
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="weather"
            element={
              <ProtectedRoute>
                <WeatherPrediction />
              </ProtectedRoute>
            }
          />
          <Route
            path="carbon"
            element={
              <ProtectedRoute>
                <CarbonFootprint />
              </ProtectedRoute>
            }
          />
          <Route
            path="urban"
            element={
              <ProtectedRoute>
                <UrbanPlanning />
              </ProtectedRoute>
            }
          />
        </Route>
      </Routes>
    </AuthProvider>
  )
}

export default App
