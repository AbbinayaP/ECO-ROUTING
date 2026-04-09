import { ResponsiveContainer, RadialBarChart, RadialBar } from "recharts";
import { Card } from "../ui/card";

interface Props {
  score: number | null;
}

export const EcoScoreRing = ({ score }: Props) => {
  const value = score ?? 0;
  const data = [{ name: "EcoScore", value, fill: "#22c55e" }];

  return (
    <Card className="p-4 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <p className="text-xs uppercase tracking-wide text-slate-400">
          EcoScore
        </p>
        <span className="text-[10px] text-slate-500">
          w1·CO₂ + w2·Delay + w3·Distance
        </span>
      </div>
      <div className="h-40">
        <ResponsiveContainer>
          <RadialBarChart
            cx="50%"
            cy="50%"
            innerRadius="70%"
            outerRadius="100%"
            barSize={12}
            data={data}
            startAngle={220}
            endAngle={-40}
          >
            <RadialBar
              dataKey="value"
              cornerRadius={999}
              background={{ fill: "rgba(15,23,42,0.8)" }}
            />
          </RadialBarChart>
        </ResponsiveContainer>
      </div>
      <div className="text-center">
        <p className="text-3xl font-semibold text-emerald-400">
          {value.toFixed(0)}
        </p>
        <p className="text-xs text-slate-400">Eco efficiency score (0–100)</p>
      </div>
    </Card>
  );
};

