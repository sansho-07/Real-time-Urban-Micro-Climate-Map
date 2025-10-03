"use client"

import { useEffect, useRef, useState } from "react"

export interface WebSocketMessage {
  type: "connected" | "analysis_update" | "error"
  message?: string
  data?: any
}

export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null)
  const eventSourceRef = useRef<EventSource | null>(null)
  const [retryCount, setRetryCount] = useState(0)
  const maxRetries = 3

  useEffect(() => {
    const connect = () => {
      const eventSource = new EventSource(url)
      eventSourceRef.current = eventSource

      eventSource.onopen = () => {
        setIsConnected(true)
        setRetryCount(0)
      }

      eventSource.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as WebSocketMessage
          setLastMessage(message)
        } catch (error) {
          console.error("Error parsing message:", error)
        }
      }

      eventSource.onerror = () => {
        setIsConnected(false)
        eventSource.close()

        if (retryCount < maxRetries) {
          const delay = Math.min(1000 * Math.pow(2, retryCount), 10000)
          setTimeout(() => {
            setRetryCount((prev) => prev + 1)
            connect()
          }, delay)
        }
      }
    }

    connect()

    // Cleanup on unmount
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close()
        setIsConnected(false)
      }
    }
  }, [url])

  return { isConnected, lastMessage }
}
