import React, { useState } from 'react';
import { Newspaper, Zap, CheckCircle2 } from 'lucide-react';

export default function NewsAnalyzer({ onDisruptionDetected }) {
  const [newsText, setNewsText] = useState(
    "Port of Rotterdam operations came to an abrupt halt this morning as dockworkers launched an open-ended wage strike. Deliveries to BMW and Tesla Gigafactory Berlin face delays of 30 days."
  );
  const [nlpResult, setNlpResult] = useState(null);

  const analyze = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/nlp/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: newsText })
      });
      const data = await res.json();
      setNlpResult(data);
    } catch (e) {
      console.error(e);
    }
  };

  const simulate = () => {
    if (nlpResult && nlpResult.affected_node_ids) {
      onDisruptionDetected(nlpResult.affected_node_ids, nlpResult.severity_score, nlpResult.estimated_direct_delay_days);
    }
  };

  return (
    <aside className="w-80 bg-slate-900 border-r border-slate-800 p-4 flex flex-col space-y-3">
      <div className="flex items-center space-x-2">
        <Newspaper className="w-4 h-4 text-cyan-400" />
        <h2 className="text-sm font-semibold">NLP Disruption Ingestion</h2>
      </div>

      <textarea
        value={newsText}
        onChange={e => setNewsText(e.target.value)}
        className="w-full h-32 bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-200"
      />

      <button onClick={analyze} className="w-full bg-cyan-600 hover:bg-cyan-500 text-slate-950 font-bold py-1.5 rounded-lg text-xs">
        Extract Entities
      </button>

      {nlpResult && (
        <div className="bg-slate-800/60 p-3 rounded-lg text-xs space-y-1.5 border border-slate-700">
          <div className="flex justify-between">
            <span className="text-slate-400">Category:</span>
            <span className="font-semibold text-white">{nlpResult.primary_category}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Delay:</span>
            <span className="font-bold text-amber-400">~{nlpResult.estimated_direct_delay_days} Days</span>
          </div>
          <button onClick={simulate} className="mt-2 w-full bg-rose-600 hover:bg-rose-500 text-white font-bold py-1.5 rounded-lg text-xs flex items-center justify-center space-x-1">
            <Zap className="w-3.5 h-3.5" />
            <span>Simulate Ripple Effect</span>
          </button>
        </div>
      )}
    </aside>
  );
}
