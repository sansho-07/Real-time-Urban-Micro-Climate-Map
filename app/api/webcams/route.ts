import { NextResponse } from "next/server"

// Phase 1: Return predefined webcam list
// Phase 2 will add actual image fetching and CV analysis
export async function GET() {
  const webcams = [
    {
      id: "cam-1",
      name: "Downtown Plaza",
      location: { lat: 40.7589, lng: -73.9851 },
      url: "https://example.com/cam1",
    },
    {
      id: "cam-2",
      name: "Central Park North",
      location: { lat: 40.7967, lng: -73.9496 },
      url: "https://example.com/cam2",
    },
    {
      id: "cam-3",
      name: "Brooklyn Bridge",
      location: { lat: 40.7061, lng: -73.9969 },
      url: "https://example.com/cam3",
    },
    {
      id: "cam-4",
      name: "Times Square",
      location: { lat: 40.758, lng: -73.9855 },
      url: "https://example.com/cam4",
    },
    {
      id: "cam-5",
      name: "Hudson Yards",
      location: { lat: 40.7536, lng: -74.0014 },
      url: "https://example.com/cam5",
    },
    {
      id: "cam-6",
      name: "East River Park",
      location: { lat: 40.7155, lng: -73.9742 },
      url: "https://example.com/cam6",
    },
    {
      id: "cam-7",
      name: "Financial District",
      location: { lat: 40.7074, lng: -74.0113 },
      url: "https://example.com/cam7",
    },
    {
      id: "cam-8",
      name: "Upper West Side",
      location: { lat: 40.787, lng: -73.9754 },
      url: "https://example.com/cam8",
    },
    {
      id: "cam-9",
      name: "Queens Plaza",
      location: { lat: 40.7489, lng: -73.9372 },
      url: "https://example.com/cam9",
    },
    {
      id: "cam-10",
      name: "Williamsburg",
      location: { lat: 40.7081, lng: -73.9571 },
      url: "https://example.com/cam10",
    },
  ]

  return NextResponse.json({ webcams })
}
