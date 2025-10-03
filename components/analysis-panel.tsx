"use client"

import { Card } from "@/components/ui/card"
import { Sun, Droplets, TrendingUp, TrendingDown } from "lucide-react"
import { useEffect, useState } from "react"

interface AnalysisStats {
  avgSunExposure: number
  avgWetness: number
  sunTrend: "up" | "down" | "stable"
  wetnessTrend: "up" | "down" | "stable"
}

export function AnalysisPanel() {
  const [stats, setStats] = useState<AnalysisStats>({
    avgSunExposure: 0.68,
    avgWetness: 0.15,
    sunTrend: "stable",
    wetnessTrend: "down",
  })

  useEffect(() => {
    // Simulate real-time stats updates
    const interval = setInterval(() => {
      setStats((prev) => {
        const newSun = Math.max(0, Math.min(1, prev.avgSunExposure + (Math.random() - 0.5) * 0.05))
        const newWetness = Math.max(0, Math.min(1, prev.avgWetness + (Math.random() - 0.5) * 0.03))

        return {
          avgSunExposure: newSun,
          avgWetness: newWetness,
          sunTrend: newSun > prev.avgSunExposure ? "up" : newSun < prev.avgSunExposure ? "down" : "stable",
          wetnessTrend: newWetness > prev.avgWetness ? "up" : newWetness < prev.avgWetness ? "down" : "stable",
        }
      })
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-3">
      <div>
        <h3 className="text-sm font-semibold text-foreground">City-Wide Analysis</h3>
        <p className="text-xs text-muted-foreground">Aggregated micro-climate data</p>
      </div>

      <Card className="border-border bg-background p-4">
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sun className="h-4 w-4 text-accent" />
              <span className="text-sm text-muted-foreground">Avg Sun Exposure</span>
            </div>
            {stats.sunTrend === "up" ? (
              <TrendingUp className="h-4 w-4 text-green-500" />
            ) : stats.sunTrend === "down" ? (
              <TrendingDown className="h-4 w-4 text-red-500" />
            ) : null}
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-foreground">{Math.round(stats.avgSunExposure * 100)}%</span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
            <div
              className="h-full bg-accent transition-all duration-500"
              style={{ width: `${stats.avgSunExposure * 100}%` }}
            />
          </div>
        </div>
      </Card>

      <Card className="border-border bg-background p-4">
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Droplets className="h-4 w-4 text-chart-1" />
              <span className="text-sm text-muted-foreground">Avg Wetness</span>
            </div>
            {stats.wetnessTrend === "up" ? (
              <TrendingUp className="h-4 w-4 text-green-500" />
            ) : stats.wetnessTrend === "down" ? (
              <TrendingDown className="h-4 w-4 text-red-500" />
            ) : null}
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-foreground">{Math.round(stats.avgWetness * 100)}%</span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
            <div
              className="h-full bg-chart-1 transition-all duration-500"
              style={{ width: `${stats.avgWetness * 100}%` }}
            />
          </div>
        </div>
      </Card>

      <div className="rounded-lg border border-border bg-muted/30 p-3">
        <p className="text-xs font-medium text-foreground">CV Analysis Active</p>
        <p className="mt-1 text-xs text-muted-foreground">
          Using OpenCV for sun/shadow detection and wetness analysis via reflection and surface darkness detection.
        </p>
      </div>
    </div>
  )
}
