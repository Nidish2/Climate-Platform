import type React from "react"
import { type LucideIcon, TrendingUp, TrendingDown } from "lucide-react"

interface MetricCardProps {
  title: string
  value: string | number
  change: string
  icon: LucideIcon
  trend: "up" | "down"
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, change, icon: Icon, trend }) => {
  const TrendIcon = trend === "up" ? TrendingUp : TrendingDown
  const trendColor = trend === "up" ? "text-red-600" : "text-green-600"

  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
        <div className="p-3 bg-primary-50 rounded-lg">
          <Icon className="h-6 w-6 text-primary-600" />
        </div>
      </div>
      <div className="flex items-center mt-4">
        <TrendIcon className={`h-4 w-4 ${trendColor}`} />
        <span className={`text-sm font-medium ml-1 ${trendColor}`}>{change}</span>
        <span className="text-sm text-gray-600 ml-2">from last month</span>
      </div>
    </div>
  )
}

export default MetricCard
