"use client"

import { Card } from "@/components/ui/card"
import { Camera, MapPin, Activity, Clock } from "lucide-react"
import { useEffect, useState } from "react"
import { AnalysisPanel } from "./analysis-panel"
import { useWebSocket } from "@/hooks/use-websocket"

export function StatsPanel() {
  const [stats, setStats] = useState({
    activeCameras: 0,
    locations: 0,
    lastUpdate: new Date(),
    analysisRate: 0,
  })

  const { isConnected, lastMessage } = useWebSocket("/api/ws")

  useEffect(() => {
    // Update stats when WebSocket messages arrive
    if (lastMessage && lastMessage.type === "analysis_update") {
      setStats((prev) => ({
        ...prev,
        lastUpdate: new Date(),
        analysisRate: Math.floor(Math.random() * 5) + 15,
      }))
    }
  }, [lastMessage])

  useEffect(() => {
    // Initial stats
    setStats({
      activeCameras: 10,
      locations: 10,
      lastUpdate: new Date(),
      analysisRate: 18,
    })
  }, [])

  return (
    <aside className="w-80 border-r border-border bg-card p-4">
      <div className="space-y-4">
        <div>
          <h2 className="text-sm font-semibold text-foreground">System Overview</h2>
          <p className="text-xs text-muted-foreground">Live monitoring statistics</p>
        </div>

        <div className="space-y-3">
          <Card className="border-border bg-background p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <Camera className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Active Cameras</p>
                  <p className="text-2xl font-bold text-foreground">{stats.activeCameras}</p>
                </div>
              </div>
            </div>
          </Card>

          <Card className="border-border bg-background p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent/10">
                  <MapPin className="h-5 w-5 text-accent" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Locations</p>
                  <p className="text-2xl font-bold text-foreground">{stats.locations}</p>
                </div>
              </div>
            </div>
          </Card>

          <Card className="border-border bg-background p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-chart-3/10">
                  <Activity className="h-5 w-5 text-chart-3" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Analysis Rate</p>
                  <p className="text-2xl font-bold text-foreground">{stats.analysisRate}/min</p>
                </div>
              </div>
            </div>
          </Card>

          <Card className="border-border bg-background p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-muted">
                  <Clock className="h-5 w-5 text-muted-foreground" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Last Update</p>
                  <p className="text-sm font-medium text-foreground">{stats.lastUpdate.toLocaleTimeString()}</p>
                </div>
              </div>
            </div>
          </Card>
        </div>

        <AnalysisPanel />

        <div className="rounded-lg border border-border bg-muted/50 p-4">
          <h3 className="mb-2 text-xs font-semibold text-foreground">Data Pipeline Status</h3>
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">Image Ingestion</span>
              <span className="flex items-center gap-1 text-green-500">
                <div className="h-1.5 w-1.5 rounded-full bg-green-500" />
                Active
              </span>
            </div>
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">CV Analysis</span>
              <span className="flex items-center gap-1 text-green-500">
                <div className="h-1.5 w-1.5 rounded-full bg-green-500" />
                Active
              </span>
            </div>
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">WebSocket</span>
              <span className={`flex items-center gap-1 ${isConnected ? "text-green-500" : "text-yellow-500"}`}>
                <div className={`h-1.5 w-1.5 rounded-full ${isConnected ? "bg-green-500" : "bg-yellow-500"}`} />
                {isConnected ? "Connected" : "Connecting"}
              </span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
