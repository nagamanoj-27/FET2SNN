import React, { useState } from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, LineChart, Line } from 'recharts';
import { Zap, Clock, Target, TrendingUp } from 'lucide-react';

// Tailwind custom keyframes/utilities can be added to tailwind.config.js
// but we inline inline styles for animations where necessary to ensure instant compatibility.

export default function SNNPerformanceCore() {
  // Donut chart data (Accuracy and remaining)
  const accuracyData = [
    { name: 'Accuracy', value: 88.42 },
    { name: 'Remaining', value: 11.58 },
  ];

  // Sparkline data showing the last 5 inference runs
  const sparklineData = [
    { run: 1, acc: 86.2 },
    { run: 2, acc: 87.5 },
    { run: 3, acc: 87.1 },
    { run: 4, acc: 88.0 },
    { run: 5, acc: 88.42 },
  ];

  // Energy gauge data (0.1 pJ/spike is filled, assuming 1.0 pJ is max capacity)
  const energyGaugeData = [
    { value: 0.1 },
    { value: 0.9 }, // empty space
  ];

  // Hover state for interactive scale/glow effects
  const [hoveredCard, setHoveredCard] = useState(null);

  // Constants
  const colors = {
    gaugeGradient: ['#fbbf24', '#f97316'], // Yellow to Orange
    cyanBlue: ['#06b6d4', '#3b82f6'],      // Cyan to Blue
    purplePink: ['#8b5cf6', '#ec4899'],    // Purple to Pink
  };

  return (
    <div className="min-h-screen bg-[#0F0A1E] flex items-center justify-center p-6 font-sans">
      {/* Container holding the Core */}
      <div className="w-full max-w-5xl bg-white/10 backdrop-blur-md border border-white/20 rounded-3xl p-8 relative overflow-hidden shadow-[0_20px_50px_rgba(139,92,246,0.15)]">
        {/* Subtle background radial ambient glow */}
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-purple-600/20 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-pink-600/20 rounded-full blur-[100px] pointer-events-none" />

        {/* Section Header */}
        <div className="mb-8 border-b border-white/10 pb-4 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-extrabold tracking-tight text-white flex items-center gap-3">
              <span className="w-2 h-6 bg-purple-500 rounded-full inline-block" />
              SNN PERFORMANCE CORE
            </h2>
            <p className="text-slate-400 text-xs mt-1">Real-time neuromorphic efficiency & classification diagnostics</p>
          </div>
          <div className="px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-xs text-purple-400 font-semibold flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            LIVE INFERENCE ACTIVE
          </div>
        </div>

        {/* Grid layout for cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Card 1: Energy / Spike */}
          <div
            className={`relative rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 p-6 flex flex-col justify-between transition-all duration-300 cursor-pointer overflow-hidden group ${
              hoveredCard === 'energy'
                ? 'transform -translate-y-2 border-orange-500/40 shadow-[0_10px_30px_rgba(249,115,22,0.25)]'
                : 'shadow-xl'
            }`}
            onMouseEnter={() => setHoveredCard('energy')}
            onMouseLeave={() => setHoveredCard(null)}
          >
            {/* Ambient indicator */}
            <div className="absolute top-0 right-0 w-24 h-24 bg-orange-600/10 rounded-full blur-2xl pointer-events-none group-hover:bg-orange-600/20 transition-all duration-300" />
            
            <div className="flex justify-between items-start">
              <div>
                <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">Energy Efficiency</p>
                <h3 className="text-white text-lg font-semibold mt-1">Energy / Spike</h3>
              </div>
              <div className="p-2 rounded-xl bg-orange-500/10 border border-orange-500/20 text-orange-400 group-hover:scale-110 transition-transform duration-300">
                <Zap className="w-5 h-5 animate-[bounce_1.5s_infinite]" />
              </div>
            </div>

            {/* Visualizer: Semi-Circle Gauge */}
            <div className="h-28 w-full flex items-center justify-center mt-4 relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <defs>
                    <linearGradient id="energyGrad" x1="0" y1="0" x2="1" y2="0">
                      <stop offset="0%" stopColor={colors.gaugeGradient[0]} />
                      <stop offset="100%" stopColor={colors.gaugeGradient[1]} />
                    </linearGradient>
                  </defs>
                  <Pie
                    data={energyGaugeData}
                    startAngle={180}
                    endAngle={0}
                    cx="50%"
                    cy="85%"
                    innerRadius={52}
                    outerRadius={66}
                    paddingAngle={0}
                    dataKey="value"
                    stroke="none"
                  >
                    <Cell fill="url(#energyGrad)" />
                    <Cell fill="rgba(255, 255, 255, 0.05)" />
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute bottom-2 flex flex-col items-center">
                <span className="text-2xl font-black text-white">0.1</span>
                <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">pJ / spike</span>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-white/5 text-xs text-slate-400 flex justify-between items-center">
              <span>Dynamic leakage:</span>
              <span className="text-orange-400 font-semibold font-mono">14.2 fJ/step</span>
            </div>
          </div>

          {/* Card 2: Inference Latency */}
          <div
            className={`relative rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 p-6 flex flex-col justify-between transition-all duration-300 cursor-pointer overflow-hidden group ${
              hoveredCard === 'latency'
                ? 'transform -translate-y-2 border-cyan-500/40 shadow-[0_10px_30px_rgba(6,182,212,0.25)]'
                : 'shadow-xl'
            }`}
            onMouseEnter={() => setHoveredCard('latency')}
            onMouseLeave={() => setHoveredCard(null)}
          >
            {/* Ambient indicator */}
            <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-600/10 rounded-full blur-2xl pointer-events-none group-hover:bg-cyan-600/20 transition-all duration-300" />

            <div className="flex justify-between items-start">
              <div>
                <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">Temporal Speed</p>
                <h3 className="text-white text-lg font-semibold mt-1">Inference Latency</h3>
              </div>
              <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 group-hover:scale-110 transition-transform duration-300">
                <Clock className="w-5 h-5 animate-pulse" />
              </div>
            </div>

            {/* Visualizer: Speedometer / Horizontal Progress Bar */}
            <div className="my-auto py-6">
              <div className="flex justify-between items-baseline mb-2">
                <span className="text-5xl font-black text-white tracking-tight font-mono animate-pulse">
                  30 <span className="text-2xl font-medium text-cyan-400">µs</span>
                </span>
                <span className="text-xs text-green-400 font-bold bg-green-400/10 px-2 py-0.5 rounded border border-green-400/20">FAST</span>
              </div>
              {/* Progress track */}
              <div className="w-full h-3 bg-white/5 rounded-full overflow-hidden border border-white/5 p-[1px]">
                <div
                  className="h-full bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full transition-all duration-500 shadow-[0_0_10px_rgba(6,182,212,0.5)]"
                  style={{ width: '30%' }}
                />
              </div>
              <div className="flex justify-between text-[10px] text-slate-400 font-mono mt-1.5">
                <span>0 µs</span>
                <span>100 µs (Max)</span>
              </div>
            </div>

            <div className="pt-3 border-t border-white/5 text-xs text-slate-400 flex justify-between items-center">
              <span>Time-to-first-spike:</span>
              <span className="text-cyan-400 font-semibold font-mono">1.2 µs</span>
            </div>
          </div>

          {/* Card 3: SNN Accuracy (The Hero) */}
          <div
            className={`relative rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 p-6 flex flex-col justify-between transition-all duration-300 cursor-pointer overflow-hidden col-span-1 group ${
              hoveredCard === 'accuracy'
                ? 'transform -translate-y-2 border-purple-500/40 shadow-[0_10px_30px_rgba(139,92,246,0.25)]'
                : 'shadow-xl'
            }`}
            onMouseEnter={() => setHoveredCard('accuracy')}
            onMouseLeave={() => setHoveredCard(null)}
          >
            {/* Ambient indicator */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-purple-600/10 rounded-full blur-3xl pointer-events-none group-hover:bg-purple-600/20 transition-all duration-300" />

            <div className="flex justify-between items-start">
              <div>
                <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">Classification</p>
                <h3 className="text-white text-lg font-semibold mt-1">SNN Accuracy</h3>
              </div>
              <div className="p-2 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400 group-hover:scale-110 transition-transform duration-300">
                <Target className="w-5 h-5" />
              </div>
            </div>

            {/* Visualizer: Donut Chart and center percentage text */}
            <div className="h-32 w-full flex items-center justify-center mt-3 relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <defs>
                    <linearGradient id="accuracyGrad" x1="0" y1="0" x2="1" y2="1">
                      <stop offset="0%" stopColor={colors.purplePink[0]} />
                      <stop offset="100%" stopColor={colors.purplePink[1]} />
                    </linearGradient>
                  </defs>
                  <Pie
                    data={accuracyData}
                    innerRadius={46}
                    outerRadius={56}
                    startAngle={90}
                    endAngle={-270}
                    paddingAngle={2}
                    dataKey="value"
                    stroke="none"
                  >
                    <Cell fill="url(#accuracyGrad)" />
                    <Cell fill="rgba(255, 255, 255, 0.05)" />
                  </Pie>
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        return (
                          <div className="bg-[#1A112C] border border-purple-500/30 px-3 py-1.5 rounded-lg shadow-xl text-xs text-white">
                            <span className="font-semibold">{payload[0].name}: </span>
                            <span className="font-mono text-purple-400">{payload[0].value.toFixed(2)}%</span>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute flex flex-col items-center">
                <span className="text-2xl font-black text-white tracking-tight">88.42%</span>
                <span className="text-[9px] text-slate-400 font-bold uppercase tracking-wider">Top-1 Acc</span>
              </div>
            </div>

            {/* Sparkline Visual (Last 5 Runs) */}
            <div className="mt-4 pt-3 border-t border-white/5">
              <div className="flex justify-between items-center text-[10px] text-slate-400 mb-1.5 font-bold uppercase tracking-wider">
                <span className="flex items-center gap-1"><TrendingUp className="w-3 h-3 text-purple-400" /> Last 5 Runs</span>
                <span className="text-purple-400 font-mono">+2.22%</span>
              </div>
              <div className="h-10 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={sparklineData}>
                    <Line
                      type="monotone"
                      dataKey="acc"
                      stroke="#8b5cf6"
                      strokeWidth={2}
                      dot={{ fill: '#ec4899', r: 3, strokeWidth: 0 }}
                      activeDot={{ r: 5, strokeWidth: 0 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

          </div>
          
        </div>
      </div>
    </div>
  );
}
