"use client"

import type { WebcamData } from "@/types/webcam"

interface WebcamMarkerProps {
  data: WebcamData
  onClick: () => void
}

export function WebcamMarker({ data, onClick }: WebcamMarkerProps) {
  const getSunColor = (exposure: number) => {
    if (exposure > 0.7) return "bg-accent"
    if (exposure > 0.4) return "bg-orange-500"
    return "bg-slate-400"
  }

  return (
    <button
      onClick={onClick}
      className={`flex h-10 w-10 items-center justify-center rounded-full border-2 border-white/30 text-xs font-bold text-black shadow-lg transition-transform hover:scale-110 ${getSunColor(data.sunExposure)}`}
    >
      {Math.round(data.sunExposure * 100)}%
    </button>
  )
}
