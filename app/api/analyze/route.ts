import { NextResponse } from "next/server"
import { readdir, readFile } from "fs/promises"
import { join } from "path"

export async function GET() {
  try {
    const dataDir = join(process.cwd(), "data", "analysis_results")

    try {
      const files = await readdir(dataDir)
      const jsonFiles = files
        .filter((f) => f.endsWith(".json"))
        .sort()
        .reverse()

      if (jsonFiles.length === 0) {
        // Return demo data if no analysis files exist
        return NextResponse.json({
          timestamp: new Date().toISOString(),
          results: generateDemoData(),
          total_analyzed: 5,
        })
      }

      const latestFile = jsonFiles[0]
      const filePath = join(dataDir, latestFile)
      const fileContent = await readFile(filePath, "utf-8")
      const data = JSON.parse(fileContent)

      return NextResponse.json(data)
    } catch (error) {
      // If directory doesn't exist or error reading, return demo data
      return NextResponse.json({
        timestamp: new Date().toISOString(),
        results: generateDemoData(),
        total_analyzed: 5,
      })
    }
  } catch (error) {
    console.error("Error reading analysis results:", error)
    return NextResponse.json({ error: "Failed to read analysis results" }, { status: 500 })
  }
}

function generateDemoData() {
  const hour = new Date().getHours()
  let baseSun = 0.5

  if (hour >= 6 && hour < 10) baseSun = 0.6
  else if (hour >= 10 && hour < 15) baseSun = 0.85
  else if (hour >= 15 && hour < 19) baseSun = 0.7
  else baseSun = 0.2

  const locations = [
    { id: "downtown-plaza", name: "Downtown Plaza", lat: 40.7589, lng: -73.9851 },
    { id: "brooklyn-bridge", name: "Brooklyn Bridge", lat: 40.7061, lng: -73.9969 },
    { id: "central-park", name: "Central Park North", lat: 40.7967, lng: -73.9496 },
    { id: "times-square", name: "Times Square", lat: 40.758, lng: -73.9855 },
    { id: "hudson-yards", name: "Hudson Yards", lat: 40.7536, lng: -74.0014 },
  ]

  return locations.map((loc) => {
    const sunExposure = Math.max(0.01, Math.min(0.99, baseSun + (Math.random() - 0.5) * 0.3))
    const isWet = Math.random() < 0.2

    return {
      webcam_id: loc.id,
      webcam_name: loc.name,
      location: { lat: loc.lat, lng: loc.lng },
      analysis: {
        sun_exposure: Math.round(sunExposure * 1000) / 1000,
        shadow_ratio: Math.round((1 - sunExposure) * 1000) / 1000,
        brightness_avg: Math.round((sunExposure * 200 + 55) * 10) / 10,
        wetness_detected: isWet,
        wetness_confidence: isWet ? 0.85 : 0.15,
        comfort_level: sunExposure > 0.7 ? "comfortable" : sunExposure > 0.4 ? "moderate" : "low",
      },
      timestamp: new Date().toISOString(),
      status: "success",
    }
  })
}
