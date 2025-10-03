"use client"

import { useEffect, useRef, useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { WebcamData } from "@/types/webcam"
import { useWebSocket } from "@/hooks/use-websocket"
import { Layers, MapIcon } from "lucide-react"

const WEBCAM_LOCATIONS: WebcamData[] = [
  {
    id: "cam-1",
    name: "Downtown Plaza",
    location: { lat: 40.7589, lng: -73.9851 },
    url: "https://example.com/cam1",
    sunExposure: 0.75,
    wetness: 0.1,
    lastUpdate: new Date(),
  },
  {
    id: "cam-2",
    name: "Central Park North",
    location: { lat: 40.7967, lng: -73.9496 },
    url: "https://example.com/cam2",
    sunExposure: 0.85,
    wetness: 0.05,
    lastUpdate: new Date(),
  },
  {
    id: "cam-3",
    name: "Brooklyn Bridge",
    location: { lat: 40.7061, lng: -73.9969 },
    url: "https://example.com/cam3",
    sunExposure: 0.45,
    wetness: 0.3,
    lastUpdate: new Date(),
  },
  {
    id: "cam-4",
    name: "Times Square",
    location: { lat: 40.758, lng: -73.9855 },
    url: "https://example.com/cam4",
    sunExposure: 0.55,
    wetness: 0.15,
    lastUpdate: new Date(),
  },
  {
    id: "cam-5",
    name: "Hudson Yards",
    location: { lat: 40.7536, lng: -74.0014 },
    url: "https://example.com/cam5",
    sunExposure: 0.92,
    wetness: 0.02,
    lastUpdate: new Date(),
  },
  {
    id: "cam-6",
    name: "East River Park",
    location: { lat: 40.7155, lng: -73.9742 },
    url: "https://example.com/cam6",
    sunExposure: 0.68,
    wetness: 0.25,
    lastUpdate: new Date(),
  },
  {
    id: "cam-7",
    name: "Financial District",
    location: { lat: 40.7074, lng: -74.0113 },
    url: "https://example.com/cam7",
    sunExposure: 0.38,
    wetness: 0.12,
    lastUpdate: new Date(),
  },
  {
    id: "cam-8",
    name: "Upper West Side",
    location: { lat: 40.787, lng: -73.9754 },
    url: "https://example.com/cam8",
    sunExposure: 0.72,
    wetness: 0.08,
    lastUpdate: new Date(),
  },
  {
    id: "cam-9",
    name: "Queens Plaza",
    location: { lat: 40.7489, lng: -73.9372 },
    url: "https://example.com/cam9",
    sunExposure: 0.81,
    wetness: 0.18,
    lastUpdate: new Date(),
  },
  {
    id: "cam-10",
    name: "Williamsburg",
    location: { lat: 40.7081, lng: -73.9571 },
    url: "https://example.com/cam10",
    sunExposure: 0.63,
    wetness: 0.22,
    lastUpdate: new Date(),
  },
]

export function ClimateMap() {
  const mapRef = useRef<HTMLDivElement>(null)
  const [webcams, setWebcams] = useState<WebcamData[]>(WEBCAM_LOCATIONS)
  const [selectedWebcam, setSelectedWebcam] = useState<WebcamData | null>(null)
  const [mapLoaded, setMapLoaded] = useState(false)
  const mapInstanceRef = useRef<any>(null)
  const markersRef = useRef<any[]>([])
  const [showHeatmap, setShowHeatmap] = useState(false)
  const heatmapLayerRef = useRef<any>(null)
  const leafletRef = useRef<any>(null)

  const { isConnected, lastMessage } = useWebSocket("/api/ws")

  useEffect(() => {
    if (lastMessage && lastMessage.type === "analysis_update") {
      const updates = lastMessage.data
      if (Array.isArray(updates)) {
        setWebcams((prev) =>
          prev.map((cam) => {
            const update = updates.find((u) => u.webcamId === cam.id)
            if (update) {
              return {
                ...cam,
                sunExposure: update.sunExposure,
                wetness: update.wetness,
                lastUpdate: new Date(update.timestamp),
              }
            }
            return cam
          }),
        )
      }
    }
  }, [lastMessage])

  useEffect(() => {
    const loadLeaflet = async () => {
      if (typeof window === "undefined") return

      const link = document.createElement("link")
      link.rel = "stylesheet"
      link.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
      document.head.appendChild(link)

      const L = await import("leaflet")
      leafletRef.current = L

      if (mapRef.current && !mapInstanceRef.current) {
        const map = L.map(mapRef.current).setView([40.7589, -73.9851], 12)

        L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
          attribution: "©OpenStreetMap, ©CartoDB",
          maxZoom: 19,
        }).addTo(map)

        mapInstanceRef.current = map

        webcams.forEach((webcam) => {
          const sunColor = webcam.sunExposure > 0.7 ? "#facc15" : webcam.sunExposure > 0.4 ? "#fb923c" : "#94a3b8"

          const icon = L.divIcon({
            className: "custom-marker",
            html: `
              <div style="
                width: 40px;
                height: 40px;
                background: ${sunColor};
                border: 3px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: bold;
                color: #000;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
                cursor: pointer;
                transition: transform 0.2s;
              ">
                ${Math.round(webcam.sunExposure * 100)}%
              </div>
            `,
            iconSize: [40, 40],
            iconAnchor: [20, 20],
          })

          const marker = L.marker([webcam.location.lat, webcam.location.lng], { icon })
            .addTo(map)
            .on("click", () => {
              setSelectedWebcam(webcam)
            })

          markersRef.current.push(marker)
        })

        setMapLoaded(true)
      }
    }

    loadLeaflet()

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }
    }
  }, [])

  useEffect(() => {
    if (!mapLoaded || !mapInstanceRef.current) return

    const updateHeatmap = async () => {
      if (showHeatmap) {
        if (!window.L || !window.L.heatLayer) {
          const script = document.createElement("script")
          script.src = "https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"
          script.onload = () => {
            createHeatmap()
          }
          document.head.appendChild(script)
        } else {
          createHeatmap()
        }
      } else {
        if (heatmapLayerRef.current) {
          mapInstanceRef.current.removeLayer(heatmapLayerRef.current)
          heatmapLayerRef.current = null
        }
      }
    }

    const createHeatmap = () => {
      if (heatmapLayerRef.current) {
        mapInstanceRef.current.removeLayer(heatmapLayerRef.current)
      }

      const heatData = webcams.map((cam) => [cam.location.lat, cam.location.lng, cam.sunExposure])

      // @ts-ignore
      heatmapLayerRef.current = window.L.heatLayer(heatData, {
        radius: 50,
        blur: 40,
        maxZoom: 17,
        max: 1.0,
        gradient: {
          0.0: "#94a3b8",
          0.4: "#fb923c",
          0.7: "#facc15",
          1.0: "#fef08a",
        },
      }).addTo(mapInstanceRef.current)
    }

    updateHeatmap()
  }, [showHeatmap, mapLoaded, webcams])

  useEffect(() => {
    if (!mapLoaded || !mapInstanceRef.current || !leafletRef.current) return

    const L = leafletRef.current

    webcams.forEach((webcam, index) => {
      if (markersRef.current[index]) {
        const sunColor = webcam.sunExposure > 0.7 ? "#facc15" : webcam.sunExposure > 0.4 ? "#fb923c" : "#94a3b8"

        const icon = L.divIcon({
          className: "custom-marker",
          html: `
            <div style="
              width: 40px;
              height: 40px;
              background: ${sunColor};
              border: 3px solid rgba(255, 255, 255, 0.3);
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              font-size: 12px;
              font-weight: bold;
              color: #000;
              box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
              cursor: pointer;
              transition: transform 0.2s;
            ">
              ${Math.round(webcam.sunExposure * 100)}%
            </div>
          `,
          iconSize: [40, 40],
          iconAnchor: [20, 20],
        })

        markersRef.current[index].setIcon(icon)
      }
    })

    if (selectedWebcam) {
      const updatedWebcam = webcams.find((w) => w.id === selectedWebcam.id)
      if (updatedWebcam) {
        setSelectedWebcam(updatedWebcam)
      }
    }
  }, [webcams, mapLoaded, selectedWebcam])

  return (
    <div className="relative h-full w-full">
      <div ref={mapRef} className="h-full w-full" />

      <div className="absolute left-4 top-4 rounded-lg border border-border bg-card px-3 py-2 shadow-lg">
        <div className="flex items-center gap-2 text-xs">
          <div className={`h-2 w-2 rounded-full ${isConnected ? "animate-pulse bg-green-500" : "bg-red-500"}`} />
          <span className="text-foreground">{isConnected ? "Live Updates Active" : "Connecting..."}</span>
        </div>
      </div>

      <div className="absolute right-4 top-4 flex gap-2">
        <Button
          variant={showHeatmap ? "default" : "outline"}
          size="sm"
          onClick={() => setShowHeatmap(!showHeatmap)}
          className="shadow-lg"
        >
          <Layers className="mr-2 h-4 w-4" />
          {showHeatmap ? "Hide Heatmap" : "Show Heatmap"}
        </Button>
      </div>

      {selectedWebcam && (
        <Card className="absolute right-4 top-16 w-80 border-border bg-card p-4 shadow-lg">
          <div className="space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-semibold text-foreground">{selectedWebcam.name}</h3>
                <p className="text-xs text-muted-foreground">
                  {selectedWebcam.location.lat.toFixed(4)}, {selectedWebcam.location.lng.toFixed(4)}
                </p>
              </div>
              <button onClick={() => setSelectedWebcam(null)} className="text-muted-foreground hover:text-foreground">
                ✕
              </button>
            </div>

            <div className="space-y-2">
              <div>
                <div className="mb-1 flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Sun Exposure</span>
                  <span className="font-semibold text-accent">{Math.round(selectedWebcam.sunExposure * 100)}%</span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
                  <div
                    className="h-full bg-accent transition-all duration-500"
                    style={{ width: `${selectedWebcam.sunExposure * 100}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="mb-1 flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Wetness</span>
                  <span className="font-semibold text-chart-1">{Math.round(selectedWebcam.wetness * 100)}%</span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
                  <div
                    className="h-full bg-chart-1 transition-all duration-500"
                    style={{ width: `${selectedWebcam.wetness * 100}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="space-y-2 rounded-lg bg-muted/50 p-3">
              <div className="flex items-center justify-between text-xs">
                <span className="text-muted-foreground">Comfort Level</span>
                <span className="font-medium text-foreground">
                  {selectedWebcam.sunExposure > 0.7 && selectedWebcam.wetness < 0.2
                    ? "Excellent"
                    : selectedWebcam.sunExposure > 0.4 && selectedWebcam.wetness < 0.3
                      ? "Good"
                      : "Fair"}
                </span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-muted-foreground">Last Updated</span>
                <span className="font-medium text-foreground">{selectedWebcam.lastUpdate.toLocaleTimeString()}</span>
              </div>
            </div>
          </div>
        </Card>
      )}

      <div className="absolute bottom-4 left-4 rounded-lg border border-border bg-card p-4 shadow-lg">
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <MapIcon className="h-4 w-4 text-foreground" />
            <p className="text-sm font-semibold text-foreground">Sun Exposure Legend</p>
          </div>
          <div className="space-y-2">
            <div className="flex items-center gap-3 text-xs">
              <div className="h-5 w-5 rounded-full bg-[#facc15] shadow-sm" />
              <span className="text-muted-foreground">High (70-100%)</span>
            </div>
            <div className="flex items-center gap-3 text-xs">
              <div className="h-5 w-5 rounded-full bg-[#fb923c] shadow-sm" />
              <span className="text-muted-foreground">Medium (40-70%)</span>
            </div>
            <div className="flex items-center gap-3 text-xs">
              <div className="h-5 w-5 rounded-full bg-[#94a3b8] shadow-sm" />
              <span className="text-muted-foreground">Low (0-40%)</span>
            </div>
          </div>
          {showHeatmap && (
            <div className="mt-3 border-t border-border pt-3">
              <p className="text-xs text-muted-foreground">Heatmap shows sun exposure intensity across the city</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
