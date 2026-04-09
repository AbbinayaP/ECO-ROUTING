import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, ChevronUp, MapPin, Footprints, Car, Bike, Train, Bus, Zap, Info } from "lucide-react";
import { Card } from "../ui/card";

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

interface Comparison {
  emission_saved_pct: number;
  extra_travel_time_min: number;
}

interface Props {
  fastest: RouteOption | null;
  eco: RouteOption | null;
  comparison: Comparison | null;
}

const getModeIcon = (mode: string) => {
  switch (mode.toLowerCase()) {
    case "walking": return Footprints;
    case "bicycling": return Bike;
    case "transit": return Train;
    case "bus": return Bus;
    case "driving": return Car;
    case "ev": return Zap;
    default: return MapPin;
  }
};

export const RouteComparisonCards = ({ fastest, eco, comparison }: Props) => {
  const [showBreakdown, setShowBreakdown] = useState(false);

  if (!fastest || !eco || !comparison) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card className="h-32 flex items-center justify-center text-sm text-slate-500">
          Run a query to compare fastest vs eco‑optimized routes.
        </Card>
        <Card className="h-32" />
      </div>
    );
  }

  const cards = [
    {
      label: "Fastest route",
      accent: "text-sky-400",
      option: fastest,
      canExpand: true
    },
    {
      label: "Eco‑optimized route",
      accent: "text-emerald-400",
      option: eco,
      canExpand: false
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-start">
      {cards.map(({ label, accent, option, canExpand }, idx) => (
        <motion.div
          key={label}
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05 * idx }}
          className="flex flex-col gap-2"
        >
          <Card className={`p-4 space-y-2 relative overflow-hidden ${canExpand ? 'ring-1 ring-sky-500/20' : ''}`}>
            <p className={`text-xs font-medium ${accent}`}>{label}</p>
            <p className="text-xs text-slate-400">
              {option.mode.toUpperCase()} •{" "}
              {option.distance_km.toFixed(2)} km •{" "}
              {option.duration_in_traffic_min.toFixed(1)} min in traffic
            </p>
            <div className="grid grid-cols-3 gap-2 text-xs mt-2">
              <div className="space-y-0.5">
                <p className="text-slate-400">CO₂</p>
                <p className="font-semibold text-slate-100">
                  {option.co2_kg.toFixed(2)} kg
                </p>
              </div>
              <div className="space-y-0.5">
                <p className="text-slate-400">Delay</p>
                <p className="font-semibold text-slate-100">
                  {option.traffic_delay_min.toFixed(1)} min
                </p>
              </div>
              <div className="space-y-0.5">
                <p className="text-slate-400">EcoScore</p>
                <p className="font-semibold text-emerald-400">
                  {option.eco_score.toFixed(0)}
                </p>
              </div>
            </div>

            {idx === 1 && (
              <div className="mt-3 text-[11px] text-emerald-300/90 leading-relaxed bg-emerald-500/5 p-2 rounded-md border border-emerald-500/10">
                Saves{" "}
                <span className="font-bold">
                  {comparison.emission_saved_pct.toFixed(1)}%
                </span>{" "}
                CO₂ vs fastest, with{" "}
                <span className="font-bold">
                  {comparison.extra_travel_time_min.toFixed(1)} min
                </span>{" "}
                extra travel time.
              </div>
            )}

            {canExpand && option.steps.length > 0 && (
              <button
                onClick={() => setShowBreakdown(!showBreakdown)}
                className="mt-3 w-full flex items-center justify-center gap-1.5 py-1.5 text-[11px] font-medium text-sky-400 hover:text-sky-300 transition-colors bg-sky-500/5 rounded-md border border-sky-500/10"
              >
                {showBreakdown ? (
                  <>Hide Route Breakdown <ChevronUp className="h-3 w-3" /></>
                ) : (
                  <>View Route Breakdown <ChevronDown className="h-3 w-3" /></>
                )}
              </button>
            )}

            <AnimatePresence>
              {canExpand && showBreakdown && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="mt-4 space-y-0 pb-2">
                    {option.steps.map((step, sIdx) => {
                      const Icon = getModeIcon(step.mode);
                      const isLast = sIdx === option.steps.length - 1;
                      return (
                        <div key={sIdx} className="relative pl-6 pb-4">
                          {!isLast && (
                            <div className="absolute left-[7px] top-[14px] bottom-0 w-[1px] bg-slate-700/60" />
                          )}
                          <div className="absolute left-0 top-[3px] h-[15px] w-[15px] rounded-full bg-slate-800 border border-slate-600 flex items-center justify-center z-10">
                            <Icon className="h-2 w-2 text-sky-400" />
                          </div>
                          <div className="space-y-1">
                            <p className="text-[11px] text-slate-200 leading-snug">
                              {step.instruction}
                            </p>
                            <div className="flex items-center gap-2 text-[10px] text-slate-500">
                              <span>{step.distance}</span>
                              <span className="h-0.5 w-0.5 rounded-full bg-slate-600" />
                              <span>{step.duration}</span>
                              {step.transit_line && (
                                <>
                                  <span className="h-0.5 w-0.5 rounded-full bg-slate-600" />
                                  <span className="text-sky-400/80 font-medium">{step.transit_line}</span>
                                </>
                              )}
                            </div>
                            {(step.departure_stop || step.arrival_stop) && (
                              <p className="text-[9px] text-slate-600 italic">
                                {step.departure_stop} → {step.arrival_stop}
                              </p>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </Card>
        </motion.div>
      ))}
    </div>
  );
};

