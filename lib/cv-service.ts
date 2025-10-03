export interface AnalysisResult {
  webcamId: string
  sunExposure: number
  wetness: number
  timestamp: string
}

export async function analyzeWebcamImage(webcamId: string, imageUrl: string): Promise<AnalysisResult> {
  const response = await fetch("/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ webcamId, imageUrl }),
  })

  if (!response.ok) {
    throw new Error("Analysis failed")
  }

  return response.json()
}

export async function getLatestAnalysis(): Promise<AnalysisResult[]> {
  const response = await fetch("/api/analyze")

  if (!response.ok) {
    throw new Error("Failed to fetch analysis results")
  }

  const data = await response.json()
  return data.results
}
