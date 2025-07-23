"use client"

import type React from "react"
import { useState } from "react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { MapContainer, TileLayer, Polygon, Marker, Popup } from "react-leaflet"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts"
import { Building, Trees, Droplets, Wind, Plus, Play } from "lucide-react"
import { urbanAPI } from "../services/api"
import "leaflet/dist/leaflet.css"

const UrbanPlanning: React.FC = () => {
  const [selectedCity, setSelectedCity] = useState("")
  const [selectedScenario, setSelectedScenario] = useState("")
  const [showScenarioModal, setShowScenarioModal] = useState(false)
  const queryClient = useQueryClient()

  const { data: cities, isLoading } = useQuery({
    queryKey: ["cities"],
    queryFn: urbanAPI.getCities,
  })

  const { data: cityData } = useQuery({
    queryKey: ["city-data", selectedCity],
    queryFn: () => urbanAPI.getCityData(selectedCity),
    enabled: !!selectedCity,
  })

  const { data: scenarios } = useQuery({
    queryKey: ["scenarios", selectedCity],
    queryFn: () => urbanAPI.getScenarios(selectedCity),
    enabled: !!selectedCity,
  })

  const { data: resilienceMetrics } = useQuery({
    queryKey: ["resilience-metrics", selectedCity, selectedScenario],
    queryFn: () => urbanAPI.getResilienceMetrics(selectedCity, selectedScenario),
    enabled: !!selectedCity && !!selectedScenario,
  })

  const simulationMutation = useMutation({
    mutationFn: urbanAPI.runSimulation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resilience-metrics"] })
    },
  })

  const handleRunSimulation = () => {
    if (selectedCity && selectedScenario) {
      simulationMutation.mutate({ cityId: selectedCity, scenarioId: selectedScenario })
    }
  }

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
          <h1 className="text-3xl font-bold text-gray-900">Climate-Resilient Urban Planning</h1>
          <p className="mt-2 text-gray-600">AI-powered urban development scenario modeling and optimization</p>
        </div>

        <div className="flex space-x-4">
          <select value={selectedCity} onChange={(e) => setSelectedCity(e.target.value)} className="input-field">
            <option value="">Select City</option>
            {cities?.map((city: any) => (
              <option key={city.id} value={city.id}>
                {city.name}
              </option>
            ))}
          </select>

          {selectedCity && (
            <select
              value={selectedScenario}
              onChange={(e) => setSelectedScenario(e.target.value)}
              className="input-field"
            >
              <option value="">Select Scenario</option>
              {scenarios?.map((scenario: any) => (
                <option key={scenario.id} value={scenario.id}>
                  {scenario.name}
                </option>
              ))}
            </select>
          )}

          <button onClick={() => setShowScenarioModal(true)} className="btn-secondary">
            <Plus className="h-4 w-4 mr-2" />
            New Scenario
          </button>
        </div>
      </div>

      {selectedCity && cityData && (
        <>
          {/* City Overview */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="card">
              <div className="flex items-center">
                <Building className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Population</p>
                  <p className="text-2xl font-bold text-gray-900">{cityData.population?.toLocaleString()}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <Trees className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Green Coverage</p>
                  <p className="text-2xl font-bold text-gray-900">{cityData.greenCoverage}%</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <Droplets className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Water Security</p>
                  <p className="text-2xl font-bold text-gray-900">{cityData.waterSecurity}/10</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <Wind className="h-8 w-8 text-gray-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Air Quality Index</p>
                  <p className="text-2xl font-bold text-gray-900">{cityData.airQuality}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Urban Planning Map */}
          <div className="card">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Urban Development Map</h3>
              {selectedScenario && (
                <button onClick={handleRunSimulation} disabled={simulationMutation.isPending} className="btn-primary">
                  <Play className="h-4 w-4 mr-2" />
                  {simulationMutation.isPending ? "Running..." : "Run Simulation"}
                </button>
              )}
            </div>
            <div className="h-96 rounded-lg overflow-hidden">
              <MapContainer
                center={cityData.coordinates || [40.7128, -74.006]}
                zoom={12}
                style={{ height: "100%", width: "100%" }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />

                {/* Development Zones */}
                {cityData.developmentZones?.map((zone: any) => (
                  <Polygon
                    key={zone.id}
                    positions={zone.coordinates}
                    pathOptions={{
                      color:
                        zone.type === "green"
                          ? "#22c55e"
                          : zone.type === "residential"
                            ? "#3b82f6"
                            : zone.type === "commercial"
                              ? "#f59e0b"
                              : "#ef4444",
                      fillOpacity: 0.3,
                    }}
                  >
                    <Popup>
                      <div>
                        <h4 className="font-semibold">{zone.name}</h4>
                        <p>Type: {zone.type}</p>
                        <p>Area: {zone.area} km²</p>
                        <p>Climate Impact: {zone.climateImpact}</p>
                      </div>
                    </Popup>
                  </Polygon>
                ))}

                {/* Infrastructure Points */}
                {cityData.infrastructure?.map((item: any) => (
                  <Marker key={item.id} position={[item.lat, item.lng]}>
                    <Popup>
                      <div>
                        <h4 className="font-semibold">{item.name}</h4>
                        <p>Type: {item.type}</p>
                        <p>Resilience Score: {item.resilienceScore}/10</p>
                      </div>
                    </Popup>
                  </Marker>
                ))}
              </MapContainer>
            </div>
          </div>

          {selectedScenario && resilienceMetrics && (
            <>
              {/* Resilience Metrics */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Climate Resilience Score</h3>
                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <RadarChart data={resilienceMetrics.radarData || []}>
                        <PolarGrid />
                        <PolarAngleAxis dataKey="category" />
                        <PolarRadiusAxis angle={90} domain={[0, 10]} />
                        <Radar name="Current" dataKey="current" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
                        <Radar name="Projected" dataKey="projected" stroke="#22c55e" fill="#22c55e" fillOpacity={0.3} />
                        <Tooltip />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Impact Assessment</h3>
                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={resilienceMetrics.impactData || []}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="metric" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="before" fill="#ef4444" name="Before" />
                        <Bar dataKey="after" fill="#22c55e" name="After" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              {/* AI Recommendations */}
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">AI-Generated Planning Recommendations</h3>
                <div className="space-y-4">
                  {resilienceMetrics.recommendations?.map((rec: any, index: number) => (
                    <div key={index} className="p-4 bg-orange-50 rounded-lg">
                      <div className="flex items-start">
                        <Building className="h-5 w-5 text-orange-600 mt-0.5" />
                        <div className="ml-3 flex-1">
                          <div className="flex justify-between items-start">
                            <div>
                              <h4 className="font-medium text-orange-900">{rec.title}</h4>
                              <p className="text-orange-800 mt-1">{rec.description}</p>
                            </div>
                            <div className="text-right">
                              <p className="text-sm font-medium text-orange-900">Resilience Improvement</p>
                              <p className="text-lg font-bold text-orange-600">+{rec.resilienceImprovement}</p>
                            </div>
                          </div>
                          <div className="flex justify-between items-center mt-3">
                            <p className="text-sm text-orange-600">
                              Cost: {rec.cost} | Timeline: {rec.timeline}
                            </p>
                            <button className="btn-primary text-sm">Implement</button>
                          </div>
                        </div>
                      </div>
                    </div>
                  )) || (
                    <div className="p-4 bg-orange-50 rounded-lg">
                      <div className="flex items-start">
                        <Building className="h-5 w-5 text-orange-600 mt-0.5" />
                        <div className="ml-3 flex-1">
                          <div className="flex justify-between items-start">
                            <div>
                              <h4 className="font-medium text-orange-900">Green Infrastructure Expansion</h4>
                              <p className="text-orange-800 mt-1">
                                RAG analysis suggests implementing 25% more green roofs and urban forests to improve
                                flood resilience and reduce urban heat island effect.
                              </p>
                            </div>
                            <div className="text-right">
                              <p className="text-sm font-medium text-orange-900">Resilience Improvement</p>
                              <p className="text-lg font-bold text-orange-600">+2.3</p>
                            </div>
                          </div>
                          <div className="flex justify-between items-center mt-3">
                            <p className="text-sm text-orange-600">Cost: $15M | Timeline: 24 months</p>
                            <button className="btn-primary text-sm">Implement</button>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </>
          )}
        </>
      )}
    </div>
  )
}

export default UrbanPlanning
