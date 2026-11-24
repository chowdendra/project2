import React, { useState, useEffect } from 'react';
import GraphView from './components/GraphView';
import NewsAnalyzer from './components/NewsAnalyzer';
import PredictionPanel from './components/PredictionPanel';
import { Network, BarChart2, ShieldAlert } from 'lucide-react';

export default function App() {
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [predictions, setPredictions] = useState(null);
  const [activeDisruption, setActiveDisruption] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/graph')
      .then(res => res.json())
      .then(data => setGraphData(data))
      .catch(err => console.error('Error fetching graph:', err));
  }, []);

  const handleSimulate = (disruptedIds, severity, delay) => {
    fetch('http://localhost:8000/api/predict/ripple', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        disrupted_nodes: disruptedIds,
        severity: severity,
        initial_delay: delay
      })
    })
      .then(res => res.json())
      .then(data => {
        setPredictions(data);
        setActiveDisruption({ ids: disruptedIds, severity, delay });
      })
      .catch(err => console.error('Prediction failed:', err));
  };

  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-100">
      <header className="bg-slate-900 border-b border-slate-800 px-6 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
            <Network className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-base font-bold">AtmoGraph</h1>
            <p className="text-xs text-slate-400">Supply Chain Ripple Effect Predictor</p>
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <NewsAnalyzer onDisruptionDetected={handleSimulate} />
        <main className="flex-1 relative">
          <GraphView graphData={graphData} predictions={predictions} activeDisruption={activeDisruption} />
        </main>
        <PredictionPanel predictions={predictions} />
      </div>
    </div>
  );
}
