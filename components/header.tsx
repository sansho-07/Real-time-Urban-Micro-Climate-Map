import { Cloud, Sun, Droplets } from "lucide-react"

export function Header() {
  return (
    <header className="border-b border-border bg-card">
      <div className="flex h-16 items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
            <Cloud className="h-6 w-6 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-foreground">Urban Micro-Climate Map</h1>
            <p className="text-xs text-muted-foreground">Real-time environmental monitoring</p>
          </div>
        </div>
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 text-sm">
            <Sun className="h-4 w-4 text-accent" />
            <span className="text-muted-foreground">Sun Exposure</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Droplets className="h-4 w-4 text-chart-1" />
            <span className="text-muted-foreground">Wetness Detection</span>
          </div>
          <div className="flex items-center gap-2 rounded-full bg-muted px-3 py-1 text-xs">
            <div className="h-2 w-2 animate-pulse rounded-full bg-green-500" />
            <span className="text-foreground">Live</span>
          </div>
        </div>
      </div>
    </header>
  )
}
