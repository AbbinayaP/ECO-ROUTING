import { Leaf, Navigation, Route, Gauge, MessageCircle } from "lucide-react";
import { Card } from "../ui/card";

interface Props {
  onOpenChat?: () => void;
}

export const Sidebar = ({ onOpenChat }: Props) => {
  return (
    <aside className="w-64 shrink-0">
      <Card className="h-full p-6 flex flex-col gap-8">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-2xl bg-gradient-to-br from-emerald-400 to-sky-500 flex items-center justify-center">
            <Leaf className="h-6 w-6 text-slate-950" />
          </div>
          <div>
            <p className="font-semibold text-sm">
              ML Eco-Routing System
            </p>
          </div>
        </div>

        <nav className="space-y-3 text-sm text-slate-300">
          <div className="flex items-center gap-3">
            <Navigation className="h-4 w-4 text-sky-400" />
            <span>Multimodal route planner</span>
          </div>
          <div className="flex items-center gap-3">
            <Route className="h-4 w-4 text-emerald-400" />
            <span>Fastest vs eco-optimized</span>
          </div>
          <div className="flex items-center gap-3">
            <Gauge className="h-4 w-4 text-violet-400" />
            <span>Real-time EcoScore</span>
          </div>
        </nav>

        <div className="pt-2 border-t border-slate-800/60">
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onOpenChat?.();
            }}
            className="w-full relative z-10 flex items-center justify-center gap-2 py-2.5 rounded-lg bg-emerald-600/10 text-emerald-400 hover:bg-emerald-600/20 border border-emerald-500/20 transition-all font-medium text-sm group pointer-events-auto"
          >
            <MessageCircle className="h-4 w-4 group-hover:scale-110 transition-transform pointer-events-none" />
            <span>Ask AI Assistant</span>
          </button>
        </div>

        <div className="mt-auto text-xs text-slate-500">
          <p className="font-medium text-slate-300 mb-1">
            System highlights
          </p>
          <ul className="space-y-1 list-disc list-inside">
            <li>Random Forest emission model</li>
            <li>Google Directions + traffic</li>
            <li>SQLite route history</li>
          </ul>
        </div>
      </Card>
    </aside>
  );
};

