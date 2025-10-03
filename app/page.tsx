import { ClimateMap } from "@/components/climate-map"
import { Header } from "@/components/header"
import { StatsPanel } from "@/components/stats-panel"

export default function Home() {
  return (
    <div className="flex h-screen flex-col bg-background">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <StatsPanel />
        <main className="flex-1">
          <ClimateMap />
        </main>
      </div>
    </div>
  )
}
