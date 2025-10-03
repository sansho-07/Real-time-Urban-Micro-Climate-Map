import type { NextRequest } from "next/server"

// Server-Sent Events handler for real-time climate data updates
export async function GET(req: NextRequest) {
  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      // Send initial connection message
      const data = `data: ${JSON.stringify({ type: "connected", message: "Real-time connection established" })}\n\n`
      controller.enqueue(encoder.encode(data))

      // Simulate real-time updates every 3 seconds
      const interval = setInterval(() => {
        // Generate random analysis updates for all webcams
        const updates = Array.from({ length: 10 }, (_, i) => ({
          webcamId: `cam-${i + 1}`,
          sunExposure: Math.max(0, Math.min(1, Math.random())),
          wetness: Math.max(0, Math.min(1, Math.random() * 0.4)),
          timestamp: new Date().toISOString(),
        }))

        const message = `data: ${JSON.stringify({ type: "analysis_update", data: updates })}\n\n`
        controller.enqueue(encoder.encode(message))
      }, 3000)

      // Cleanup on close
      req.signal.addEventListener("abort", () => {
        clearInterval(interval)
        controller.close()
      })
    },
  })

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  })
}
