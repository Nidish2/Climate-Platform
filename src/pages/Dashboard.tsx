import type React from "react"
import { useQuery } from "@tanstack/react-query"
import { Link } from "react-router-dom"
import { Cloud, Leaf, Building, TrendingUp, AlertTriangle, Activity } from "lucide-react"
import { dashboardAPI } from "../services/api"
import MetricCard from "../components/MetricCard"
import RecentAlerts from "../components/RecentAlerts"

const Dashboard: React.FC = () => {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ["dashboard-metrics"],
    queryFn: dashboardAPI.getMetrics,
  })

  const { data: alerts } = useQuery({
    queryKey: ["recent-alerts"],
    queryFn: dashboardAPI.getRecentAlerts,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const moduleCards = [
    {
      title: "Weather Prediction",
      description: "AI-powered extreme weather forecasting and risk assessment",
      icon: Cloud,
      href: "/weather",
      color: "bg-blue-500",
      stats: `${metrics?.activeWeatherAlerts || 0} active alerts`,
    },
    {
      title: "Carbon Footprint",
      description: "Corporate carbon analysis and policy recommendations",
      icon: Leaf,
      href: "/carbon",
      color: "bg-green-500",
      stats: `${metrics?.companiesAnalyzed || 0} companies analyzed`,
    },
    {
      title: "Urban Planning",
      description: "Climate-resilient city planning and scenario modeling",
      icon: Building,
      href: "/urban",
      color: "bg-orange-500",
      stats: `${metrics?.planningProjects || 0} active projects`,
    },
  ]

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Climate Analysis Dashboard</h1>
        <p className="mt-2 text-gray-600">Comprehensive climate intelligence powered by AI</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard
          title="Global Temperature Anomaly"
          value={`+${metrics?.temperatureAnomaly || 0}°C`}
          change={`+${metrics?.temperatureChange || 0}%`}
          icon={TrendingUp}
          trend="up"
        />
        <MetricCard
          title="CO₂ Concentration"
          value={`${metrics?.co2Concentration || 0} ppm`}
          change={`+${metrics?.co2Change || 0}%`}
          icon={Activity}
          trend="up"
        />
        <MetricCard
          title="Climate Risk Score"
          value={metrics?.riskScore || 0}
          change={`${metrics?.riskChange || 0}%`}
          icon={AlertTriangle}
          trend="down"
        />
      </div>

      {/* Module Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {moduleCards.map((module) => {
          const Icon = module.icon
          return (
            <Link
              key={module.title}
              to={module.href}
              className="card hover:shadow-lg transition-shadow cursor-pointer group"
            >
              <div className="flex items-center">
                <div className={`p-3 rounded-lg ${module.color} text-white`}>
                  <Icon className="h-6 w-6" />
                </div>
                <div className="ml-4 flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
                    {module.title}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">{module.description}</p>
                  <p className="text-xs text-gray-500 mt-2">{module.stats}</p>
                </div>
              </div>
            </Link>
          )
        })}
      </div>

      {/* Recent Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentAlerts alerts={alerts || []} />

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Analysis Summary</h3>
          <div className="space-y-3">
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
              <div>
                <p className="text-sm text-gray-700">
                  <strong>Weather AI:</strong> Detected increased hurricane activity in Atlantic basin
                </p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
              <div>
                <p className="text-sm text-gray-700">
                  <strong>Carbon AI:</strong> Identified 15% reduction opportunity in manufacturing sector
                </p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-orange-500 rounded-full mt-2"></div>
              <div>
                <p className="text-sm text-gray-700">
                  <strong>Urban AI:</strong> Recommended green infrastructure for 3 cities
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
