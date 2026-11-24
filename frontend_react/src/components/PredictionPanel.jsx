import React from 'react';
import { Activity } from 'lucide-react';

export default function PredictionPanel({ predictions }) {
  if (!predictions) {
    return (
      <aside className="w-80 bg-slate-900 border-l border-slate-800 p-4 text-xs text-slate-500 flex items-center justify-center">
        No active simulation loaded.
      </aside>
    );
  }

  return (
    <aside className="w-80 bg-slate-900 border-l border-slate-800 p-4 flex flex-col space-y-3 overflow-y-auto">
      <div className="flex items-center space-x-2">
        <Activity className="w-4 h-4 text-rose-400" />
        <h2 className="text-sm font-semibold">Predicted Ripple Impact</h2>
      </div>

      <div className="space-y-2">
        {predictions.predictions.map(p => (
          <div key={p.node_id} className="p-2.5 bg-slate-800/50 rounded-lg border border-slate-700/60 text-xs">
            <div className="flex justify-between font-bold">
              <span>{p.name}</span>
              <span className={p.risk_level === 'High' ? 'text-rose-400' : 'text-amber-400'}>{p.risk_level}</span>
            </div>
            <div className="flex justify-between text-slate-400 mt-1">
              <span>Hop: {p.hop_distance}</span>
              <span className="text-amber-300 font-mono">+{p.predicted_delay_days} Days</span>
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
}
