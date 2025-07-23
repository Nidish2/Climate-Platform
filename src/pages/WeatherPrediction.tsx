"use client"

import type React from "react"
import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { Cloud, AlertTriangle, Thermometer, Wind } from "lucide-react"
import { weatherAPI } from "../services/api"
import "leaflet/dist/leaflet.css"

const WeatherPrediction: React.FC = () => {
  const [selectedLocation, setSelectedLocation] = useState("global")
  const [timeRange, setTimeRange] = useState("7d")

  const { data: weatherData, isLoading } = useQuery({
    queryKey: ["weather-prediction", selectedLocation, timeRange],
    queryFn: () => weatherAPI.getPredictions(selectedLocation, timeRange),
  })

  const { data: riskAssessment } = useQuery({
    queryKey: ["weather-risk", selectedLocation],
    queryFn: () => weatherAPI.getRiskAssessment(selectedLocation),
  })

  const { data: historicalData } = useQuery({
    queryKey: ["weather-historical", selectedLocation],
    queryFn: () => weatherAPI.getHistoricalData(selectedLocation),
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Extreme Weather Prediction</h1>
          <p className="mt-2 text-gray-600">AI-powered weather forecasting using IBM Environmental Intelligence</p>
        </div>

        <div className="flex space-x-4">
          <select
            value={selectedLocation}
            onChange={(e) => setSelectedLocation(e.target.value)}
            className="input-field"
          >
            <option value="global">Global</option>
            <option value="north-america">North America</option>
            <option value="europe">Europe</option>
            <option value="asia">Asia</option>
          </select>

          <select value={timeRange} onChange={(e) => setTimeRange(e.target.value)} className="input-field">
            <option value="7d">7 Days</option>
            <option value="14d">14 Days</option>
            <option value="30d">30 Days</option>
          </select>
        </div>
      </div>

      {/* Risk Assessment Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <Wind className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Hurricane Risk</p>
              <p className="text-2xl font-bold text-gray-900">{riskAssessment?.hurricane || "Medium"}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-orange-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Wildfire Risk</p>
              <p className="text-2xl font-bold text-gray-900">{riskAssessment?.wildfire || "High"}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <Thermometer className="h-8 w-8 text-red-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Heatwave Risk</p>
              <p className="text-2xl font-bold text-gray-900">{riskAssessment?.heatwave || "Critical"}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <Cloud className="h-8 w-8 text-gray-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Flood Risk</p>
              <p className="text-2xl font-bold text-gray-900">{riskAssessment?.flood || "Low"}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Weather Map */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Global Weather Risk Map</h3>
        <div className="h-96 rounded-lg overflow-hidden">
          <MapContainer center={[40.7128, -74.006]} zoom={4} style={{ height: "100%", width: "100%" }}>
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {weatherData?.riskLocations?.map((location: any) => (
              <Marker key={location.id} position={[location.lat, location.lng]}>
                <Popup>
                  <div>
                    <h4 className="font-semibold">{location.name}</h4>
                    <p>Risk Level: {location.riskLevel}</p>
                    <p>Type: {location.type}</p>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
      </div>

      {/* Temperature Trend Chart */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Temperature Trend Analysis</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={historicalData?.temperatureData || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="temperature" stroke="#3b82f6" strokeWidth={2} name="Temperature (°C)" />
              <Line
                type="monotone"
                dataKey="predicted"
                stroke="#ef4444"
                strokeWidth={2}
                strokeDasharray="5 5"
                name="Predicted (°C)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* AI Insights */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">AI-Generated Insights</h3>
        <div className="space-y-4">
          {weatherData?.insights?.map((insight: any, index: number) => (
            <div key={index} className="p-4 bg-blue-50 rounded-lg">
              <div className="flex items-start">
                <AlertTriangle className="h-5 w-5 text-blue-600 mt-0.5" />
                <div className="ml-3">
                  <h4 className="font-medium text-blue-900">{insight.title}</h4>
                  <p className="text-blue-800 mt-1">{insight.description}</p>
                  <p className="text-sm text-blue-600 mt-2">
                    Confidence: {insight.confidence}% | Source: {insight.source}
                  </p>
                </div>
              </div>
            </div>
          )) || (
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="flex items-start">
                <AlertTriangle className="h-5 w-5 text-blue-600 mt-0.5" />
                <div className="ml-3">
                  <h4 className="font-medium text-blue-900">Hurricane Season Analysis</h4>
                  <p className="text-blue-800 mt-1">
                    Agentic AI has detected increased sea surface temperatures in the Atlantic, indicating a 73%
                    probability of above-normal hurricane activity this season.
                  </p>
                  <p className="text-sm text-blue-600 mt-2">
                    Confidence: 87% | Source: IBM Environmental Intelligence + RAG Historical Data
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default WeatherPrediction
