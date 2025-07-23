import type React from "react"
import { AlertTriangle, Cloud, Thermometer, Wind } from "lucide-react"

interface Alert {
  id: string
  type: "hurricane" | "heatwave" | "wildfire" | "flood"
  severity: "low" | "medium" | "high" | "critical"
  location: string
  message: string
  timestamp: string
}

interface RecentAlertsProps {
  alerts: Alert[]
}

const RecentAlerts: React.FC<RecentAlertsProps> = ({ alerts }) => {
  const getAlertIcon = (type: Alert["type"]) => {
    switch (type) {
      case "hurricane":
        return Wind
      case "heatwave":
        return Thermometer
      case "wildfire":
        return AlertTriangle
      case "flood":
        return Cloud
      default:
        return AlertTriangle
    }
  }

  const getSeverityColor = (severity: Alert["severity"]) => {
    switch (severity) {
      case "low":
        return "bg-blue-100 text-blue-800"
      case "medium":
        return "bg-yellow-100 text-yellow-800"
      case "high":
        return "bg-orange-100 text-orange-800"
      case "critical":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Weather Alerts</h3>
      <div className="space-y-3">
        {alerts.length === 0 ? (
          <p className="text-gray-500 text-sm">No recent alerts</p>
        ) : (
          alerts.slice(0, 5).map((alert) => {
            const Icon = getAlertIcon(alert.type)
            return (
              <div key={alert.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                <Icon className="h-5 w-5 text-gray-600 mt-0.5" />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-gray-900 truncate">{alert.location}</p>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSeverityColor(alert.severity)}`}>
                      {alert.severity}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">{alert.message}</p>
                  <p className="text-xs text-gray-500 mt-1">{alert.timestamp}</p>
                </div>
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}

export default RecentAlerts
