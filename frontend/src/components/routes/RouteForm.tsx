import { useState } from "react";
import { Car, Bike, Zap, Footprints, Train, Bus, CarFront } from "lucide-react";
import { motion } from "framer-motion";
import { Button } from "../ui/button";
import { Card } from "../ui/card";

type TransportMode = "car" | "bike" | "ev" | "walking" | "metro" | "bus" | "auto";

export interface RouteFormValues {
  origin: string;
  destination: string;
  modes: TransportMode[];
  vehicle_type: TransportMode;
  fuel_type: "petrol" | "diesel" | "electric" | "none" | "cng";
  algorithm: "google" | "dijkstra" | "astar" | "multi_objective";
}

interface Props {
  onSubmit: (values: RouteFormValues) => Promise<void> | void;
  loading?: boolean;
}

const modeConfig: {
  mode: TransportMode;
  label: string;
  icon: React.ElementType;
}[] = [
    { mode: "car", label: "Car", icon: Car },
    { mode: "bike", label: "Bike", icon: Bike },
    { mode: "ev", label: "EV", icon: Zap },
    { mode: "walking", label: "Walk", icon: Footprints },
    { mode: "metro", label: "Metro", icon: Train },
    { mode: "bus", label: "Bus", icon: Bus },
    { mode: "auto", label: "Auto", icon: CarFront }
  ];

export const RouteForm = ({ onSubmit, loading }: Props) => {
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [selectedModes, setSelectedModes] = useState<TransportMode[]>([
    "car",
    "bike",
    "ev",
    "walking",
    "metro",
    "bus",
    "auto"
  ]);
  const [vehicleType, setVehicleType] = useState<TransportMode>("car");
  const [fuelType, setFuelType] = useState<"petrol" | "diesel" | "electric" | "none" | "cng">(
    "petrol"
  );
  const [algorithm, setAlgorithm] = useState<"google" | "dijkstra" | "astar" | "multi_objective">("google");

  const toggleMode = (mode: TransportMode) => {
    setSelectedModes((prev) =>
      prev.includes(mode) ? prev.filter((m) => m !== mode) : [...prev, mode]
    );
  };

  const handleVehicleChange = (v: TransportMode) => {
    setVehicleType(v);
    if (v === "ev") setFuelType("electric");
    else if (v === "walking" || v === "metro") setFuelType("none");
    else if (v === "auto") setFuelType("cng");
    else if (fuelType === "none" || fuelType === "electric") setFuelType("petrol");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!origin || !destination) return;
    await onSubmit({
      origin,
      destination,
      modes: selectedModes,
      vehicle_type: vehicleType,
      fuel_type: fuelType,
      algorithm,
    });
  };

  return (
    <Card className="p-5">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-300">
              Origin
            </label>
            <input
              className="h-10 w-full rounded-full bg-slate-900/70 border border-slate-700/70 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500/80"
              placeholder="e.g. Chennai Central"
              value={origin}
              onChange={(e) => setOrigin(e.target.value)}
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-300">
              Destination
            </label>
            <input
              className="h-10 w-full rounded-full bg-slate-900/70 border border-slate-700/70 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/80"
              placeholder="e.g. TIDEL Park"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
            />
          </div>
        </div>

        <div className="flex flex-wrap gap-2 items-center justify-between">
          <div className="flex flex-wrap gap-2">
            {modeConfig.map(({ mode, label, icon: Icon }) => {
              const active = selectedModes.includes(mode);
              return (
                <motion.button
                  type="button"
                  key={mode}
                  onClick={() => toggleMode(mode)}
                  whileTap={{ scale: 0.94 }}
                  className={`flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs border ${active
                      ? "border-emerald-400/80 bg-emerald-400/10 text-emerald-200"
                      : "border-slate-700/70 bg-slate-900/60 text-slate-400"
                    }`}
                >
                  <Icon className="h-3.5 w-3.5" />
                  <span>{label}</span>
                </motion.button>
              );
            })}
          </div>

          <div className="flex gap-2 items-center">
            <span className="text-xs text-slate-400">Vehicle</span>
            <select
              className="h-9 rounded-full bg-slate-900/80 border border-slate-700/70 text-xs px-3"
              value={vehicleType}
              onChange={(e) => handleVehicleChange(e.target.value as TransportMode)}
            >
              <option value="car">Car</option>
              <option value="bike">Bike</option>
              <option value="ev">EV</option>
              <option value="auto">Auto</option>
              <option value="bus">Bus</option>
            </select>
            <select
              className="h-9 rounded-full bg-slate-900/80 border border-slate-700/70 text-xs px-3"
              value={fuelType}
              onChange={(e) =>
                setFuelType(
                  e.target.value as "petrol" | "diesel" | "electric" | "none" | "cng"
                )
              }
            >
              <option value="petrol">Petrol</option>
              <option value="diesel">Diesel</option>
              <option value="cng">CNG</option>
              <option value="electric">Electric</option>
              <option value="none" disabled>None</option>
            </select>
          </div>
          
          <div className="flex gap-2 items-center mt-2 md:mt-0">
            <span className="text-xs text-slate-400">Algorithm</span>
            <select
              className="h-9 rounded-full bg-slate-900/80 border border-slate-700/70 text-xs px-3 focus:outline-none focus:ring-2 focus:ring-emerald-500/80"
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value as "google" | "dijkstra" | "astar" | "multi_objective")}
            >
              <option value="google">Google API (Default)</option>
              <option value="dijkstra">Local Dijkstra (OSM)</option>
              <option value="astar">Local A* (OSM)</option>
              <option value="multi_objective">Multi-Objective A* (Time + Eco)</option>
            </select>
          </div>
        </div>

        <div className="flex justify-end">
          <Button type="submit" size="lg" disabled={loading}>
            {loading ? "Computing eco routes..." : "Compute Eco-Optimized Route"}
          </Button>
        </div>
      </form>
    </Card>
  );
};

