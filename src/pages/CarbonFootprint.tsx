"use client"

import type React from "react"
import { useState } from "react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts"
import { Upload, Leaf, TrendingDown, Building2, Factory } from "lucide-react"
import { carbonAPI } from "../services/api"

const CarbonFootprint: React.FC = () => {
  const [selectedCompany, setSelectedCompany] = useState("")
  const [uploadFile, setUploadFile] = useState<File | null>(null)
  const queryClient = useQueryClient()

  const { data: companies, isLoading } = useQuery({
    queryKey: ["companies"],
    queryFn: carbonAPI.getCompanies,
  })

  const { data: carbonData } = useQuery({
    queryKey: ["carbon-data", selectedCompany],
    queryFn: () => carbonAPI.getCarbonData(selectedCompany),
    enabled: !!selectedCompany,
  })

  const { data: recommendations } = useQuery({
    queryKey: ["carbon-recommendations", selectedCompany],
    queryFn: () => carbonAPI.getRecommendations(selectedCompany),
    enabled: !!selectedCompany,
  })

  const uploadMutation = useMutation({
    mutationFn: carbonAPI.uploadCarbonData,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["companies"] })
      setUploadFile(null)
    },
  })

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setUploadFile(file)
    }
  }

  const handleUpload = () => {
    if (uploadFile) {
      uploadMutation.mutate(uploadFile)
    }
  }

  const COLORS = ["#3b82f6", "#ef4444", "#f59e0b", "#10b981", "#8b5cf6"]

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
          <h1 className="text-3xl font-bold text-gray-900">Corporate Carbon Footprint Analyzer</h1>
          <p className="mt-2 text-gray-600">AI-powered carbon analysis and policy recommendations</p>
        </div>

        <div className="flex space-x-4">
          <select value={selectedCompany} onChange={(e) => setSelectedCompany(e.target.value)} className="input-field">
            <option value="">Select Company</option>
            {companies?.map((company: any) => (
              <option key={company.id} value={company.id}>
                {company.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Upload Section */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Upload Carbon Data</h3>
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <input type="file" accept=".csv,.xlsx,.json" onChange={handleFileUpload} className="input-field" />
          </div>
          <button
            onClick={handleUpload}
            disabled={!uploadFile || uploadMutation.isPending}
            className="btn-primary disabled:opacity-50"
          >
            <Upload className="h-4 w-4 mr-2" />
            {uploadMutation.isPending ? "Uploading..." : "Upload"}
          </button>
        </div>
        <p className="text-sm text-gray-600 mt-2">
          Supported formats: CSV, Excel, JSON. Data will be processed using Data-Prep-Kit for analysis.
        </p>
      </div>

      {selectedCompany && carbonData && (
        <>
          {/* Carbon Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="card">
              <div className="flex items-center">
                <Factory className="h-8 w-8 text-gray-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Emissions</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {carbonData.totalEmissions?.toLocaleString()} tCO₂e
                  </p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <TrendingDown className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Reduction Target</p>
                  <p className="text-2xl font-bold text-gray-900">{carbonData.reductionTarget}%</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <Leaf className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Carbon Intensity</p>
                  <p className="text-2xl font-bold text-gray-900">{carbonData.carbonIntensity} tCO₂e/M$</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <Building2 className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Compliance Score</p>
                  <p className="text-2xl font-bold text-gray-900">{carbonData.complianceScore}/100</p>
                </div>
              </div>
            </div>
          </div>

          {/* Emissions Breakdown */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Emissions by Scope</h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={carbonData.emissionsByScope || []}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="scope" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="emissions" fill="#3b82f6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Emissions by Source</h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={carbonData.emissionsBySource || []}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {carbonData.emissionsBySource?.map((entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* AI Recommendations */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">AI-Generated Policy Recommendations</h3>
            <div className="space-y-4">
              {recommendations?.map((rec: any, index: number) => (
                <div key={index} className="p-4 bg-green-50 rounded-lg">
                  <div className="flex items-start">
                    <Leaf className="h-5 w-5 text-green-600 mt-0.5" />
                    <div className="ml-3 flex-1">
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="font-medium text-green-900">{rec.title}</h4>
                          <p className="text-green-800 mt-1">{rec.description}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-medium text-green-900">Potential Reduction</p>
                          <p className="text-lg font-bold text-green-600">{rec.potentialReduction}%</p>
                        </div>
                      </div>
                      <div className="flex justify-between items-center mt-3">
                        <p className="text-sm text-green-600">
                          Implementation Cost: {rec.cost} | Timeline: {rec.timeline}
                        </p>
                        <button className="btn-primary text-sm">View Details</button>
                      </div>
                    </div>
                  </div>
                </div>
              )) || (
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="flex items-start">
                    <Leaf className="h-5 w-5 text-green-600 mt-0.5" />
                    <div className="ml-3 flex-1">
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="font-medium text-green-900">Renewable Energy Transition</h4>
                          <p className="text-green-800 mt-1">
                            Agentic AI recommends transitioning 60% of energy consumption to renewable sources based on
                            regulatory analysis and cost-benefit optimization.
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-medium text-green-900">Potential Reduction</p>
                          <p className="text-lg font-bold text-green-600">35%</p>
                        </div>
                      </div>
                      <div className="flex justify-between items-center mt-3">
                        <p className="text-sm text-green-600">Implementation Cost: $2.5M | Timeline: 18 months</p>
                        <button className="btn-primary text-sm">View Details</button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Compliance Analysis */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Regulatory Compliance Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 border rounded-lg">
                <h4 className="font-medium text-gray-900">EU Taxonomy</h4>
                <p className="text-2xl font-bold text-green-600 mt-2">Compliant</p>
                <p className="text-sm text-gray-600 mt-1">87% alignment score</p>
              </div>
              <div className="p-4 border rounded-lg">
                <h4 className="font-medium text-gray-900">TCFD</h4>
                <p className="text-2xl font-bold text-yellow-600 mt-2">Partial</p>
                <p className="text-sm text-gray-600 mt-1">3/4 pillars covered</p>
              </div>
              <div className="p-4 border rounded-lg">
                <h4 className="font-medium text-gray-900">SBTi</h4>
                <p className="text-2xl font-bold text-red-600 mt-2">Non-compliant</p>
                <p className="text-sm text-gray-600 mt-1">Target validation needed</p>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default CarbonFootprint
