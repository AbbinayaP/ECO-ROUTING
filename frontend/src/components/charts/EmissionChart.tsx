import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip
} from "recharts";
import { Card } from "../ui/card";

interface EmissionHistoryItem {
  id: number;
  mode: string;
  distance_km: number;
  duration_min: number;
  traffic_delay_min: number;
  co2_kg: number;
  eco_score: number;
}

interface Props {
  items: EmissionHistoryItem[];
}

export const EmissionChart = ({ items }: Props) => {
  const data = items
    .slice()
    .reverse()
    .map((item, idx) => ({
      index: idx + 1,
      co2_kg: item.co2_kg,
      mode: item.mode
    }));

  return (
    <Card className="p-4 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <p className="text-xs uppercase tracking-wide text-slate-400">
          Emission history
        </p>
        <span className="text-[10px] text-slate-500">
          Recent eco‑routing sessions
        </span>
      </div>
      <div className="h-40">
        <ResponsiveContainer>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="co2" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22c55e" stopOpacity={0.9} />
                <stop offset="95%" stopColor="#22c55e" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            <XAxis
              dataKey="index"
              tickLine={false}
              tickMargin={8}
              tick={{ fontSize: 10, fill: "#9ca3af" }}
            />
            <YAxis
              tickLine={false}
              axisLine={false}
              tickMargin={4}
              tick={{ fontSize: 10, fill: "#9ca3af" }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(15,23,42,0.95)",
                borderRadius: 12,
                border: "1px solid rgba(148,163,184,0.5)"
              }}
              labelStyle={{ fontSize: 11, color: "#e5e7eb" }}
              itemStyle={{ fontSize: 11, color: "#a5b4fc" }}
            />
            <Area
              type="monotone"
              dataKey="co2_kg"
              stroke="#22c55e"
              fill="url(#co2)"
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
};

