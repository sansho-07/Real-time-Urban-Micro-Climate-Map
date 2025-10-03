export interface WebcamData {
  id: string
  name: string
  location: {
    lat: number
    lng: number
  }
  url: string
  sunExposure: number // 0-1 range
  wetness: number // 0-1 range
  lastUpdate: Date
}

export interface AnalysisResult {
  sunExposure: number
  wetness?: number
  timestamp: Date
}
