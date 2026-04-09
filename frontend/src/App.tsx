import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Sidebar } from "./components/layout/Sidebar";
import { RouteForm, RouteFormValues } from "./components/routes/RouteForm";
import { RouteComparisonCards } from "./components/routes/RouteComparisonCards";
import { EcoScoreRing } from "./components/charts/EcoScoreRing";
import { EmissionChart } from "./components/charts/EmissionChart";
import { ExplainableAssistant } from "./components/chat/ExplainableAssistant";

const API_BASE = "http://127.0.0.1:8000";

interface RouteStep {
  instruction: string;
  distance: string;
  duration: string;
  mode: string;
  transit_line?: string;
  departure_stop?: string;
  arrival_stop?: string;
}

interface RouteOption {
  mode: string;
  distance_km: number;
  duration_min: number;
  duration_in_traffic_min: number;
  traffic_delay_min: number;
  polyline: string;
  co2_kg: number;
  eco_score: number;
  steps: RouteStep[];
}

interface RouteComparison {
  fastest: RouteOption;
  eco_optimized: RouteOption;
  emission_saved_pct: number;
  extra_travel_time_min: number;
}

interface RouteResponse {
  origin: string;
  destination: string;
  options: RouteOption[];
  comparison: RouteComparison;
}

interface EmissionHistoryItem {
  id: number;
  mode: string;
  distance_km: number;
  duration_min: number;
  traffic_delay_min: number;
  co2_kg: number;
  eco_score: number;
}

export const App = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [route, setRoute] = useState<RouteResponse | null>(null);
  const [history, setHistory] = useState<EmissionHistoryItem[]>([]);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/emissions/history`);
      if (!res.ok) return;
      const data = await res.json();
      setHistory(data.items ?? []);
    } catch {
      // ignore history errors
    }
  };

  useEffect(() => {
    void fetchHistory();
  }, []);

  const handleSubmit = async (values: RouteFormValues) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/routes/compute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          origin: values.origin,
          destination: values.destination,
          modes: values.modes,
          vehicle_type: values.vehicle_type,
          fuel_type: values.fuel_type,
          algorithm: values.algorithm
        })
      });
      if (!res.ok) {
        const msg = await res.text();
        throw new Error(msg || "Failed to compute routes");
      }
      const data: RouteResponse = await res.json();
      setRoute(data);
      void fetchHistory();
    } catch (e: any) {
      setError(e.message ?? "Unexpected error");
    } finally {
      setLoading(false);
    }
  };

  const fastest = route?.comparison.fastest ?? null;
  const eco = route?.comparison.eco_optimized ?? null;
  const ecoScore = eco?.eco_score ?? fastest?.eco_score ?? null;
  const comparison = route
    ? {
      emission_saved_pct: route.comparison.emission_saved_pct,
      extra_travel_time_min: route.comparison.extra_travel_time_min
    }
    : null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-950 to-slate-900 text-slate-50 relative">
      <div className="mx-auto max-w-6xl px-4 py-6 md:py-8 flex gap-5">
        <Sidebar onOpenChat={() => setIsChatOpen(true)} />
        <main className="flex-1 flex flex-col gap-4">
          <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
            <div>
              <h1 className="text-xl md:text-2xl font-semibold tracking-tight">
                Machine Learning Driven Eco‑Routing
              </h1>
              <p className="text-xs text-slate-400 mt-1 max-w-xl">
                Compare fastest vs eco‑optimized routes across car, bike, EV,
                walking, metro, auto, and bus using Random Forest–based
                emission estimation and live traffic from Google Directions.
              </p>
            </div>
            {route && (
              <motion.div
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-right text-xs text-slate-400"
              >
                <p>From: {route.origin}</p>
                <p>To: {route.destination}</p>
              </motion.div>
            )}
          </header>

          <RouteForm onSubmit={handleSubmit} loading={loading} />

          {error && (
            <div className="text-xs text-rose-400 bg-rose-950/40 border border-rose-500/40 rounded-lg px-3 py-2">
              {error}
            </div>
          )}

          <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div className="lg:col-span-2">
              <RouteComparisonCards
                fastest={fastest}
                eco={eco}
                comparison={comparison}
              />
            </div>
            <EcoScoreRing score={ecoScore} />
          </section>

          <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <EmissionChart items={history} />
            {/* Placeholder for a future polyline or mode breakdown chart */}
            <div className="hidden md:block">
              <EmissionChart items={history.slice(0, 10)} />
            </div>
          </section>
        </main>
      </div>

      <ExplainableAssistant 
        routeContext={route} 
        isOpen={isChatOpen} 
        onClose={() => setIsChatOpen(false)} 
      />
    </div>
  );
};

