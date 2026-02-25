import React, { useState, useEffect } from 'react';
import { api } from '../api/client';

const PerformanceComparison = () => {
  const [dbStatus, setDbStatus] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Get database status
      const statusRes = await fetch('http://localhost:8000/api/neo4j/status');
      const statusData = await statusRes.json();
      setDbStatus(statusData);
      
      // Get performance comparison
      const perfRes = await fetch('http://localhost:8000/api/performance/compare');
      const perfData = await perfRes.json();
      setPerformance(perfData);
      
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-400">Running performance tests...</p>
        </div>
      </div>
    );
  }

  const isNeo4j = dbStatus?.status === 'connected';

  return (
    <div className="space-y-8 fade-in-up">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-4xl font-bold bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
          Database Performance Comparison
        </h2>
        <p className="text-slate-400 text-lg">Neo4j vs CSV Mode</p>
      </div>

      {/* Current Mode Card */}
      <div className={`glass rounded-2xl p-8 border-2 ${
        isNeo4j ? 'border-green-500/50' : 'border-yellow-500/50'
      }`}>
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <div className={`w-4 h-4 rounded-full ${
                isNeo4j ? 'bg-green-400 animate-pulse' : 'bg-yellow-400'
              }`}></div>
              <h3 className="text-2xl font-bold text-slate-200">
                Current Mode: {isNeo4j ? 'Neo4j Graph Database' : 'CSV In-Memory'}
              </h3>
            </div>
            <p className="text-slate-400 ml-7">
              {dbStatus?.database} - {dbStatus?.mode} Mode
            </p>
          </div>
          <div className={`text-6xl ${isNeo4j ? 'animate-pulse' : ''}`}>
            {isNeo4j ? '🚀' : '📊'}
          </div>
        </div>

        {/* Features */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3">
          {dbStatus?.features?.map((feature, index) => (
            <div key={index} className="flex items-center space-x-2 text-slate-300">
              <span className={isNeo4j ? 'text-green-400' : 'text-yellow-400'}>✓</span>
              <span>{feature}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Performance Tests */}
      <div className="glass rounded-2xl p-6 border border-slate-700/50">
        <h3 className="text-xl font-semibold text-slate-200 mb-6 flex items-center">
          <span className="w-2 h-2 bg-indigo-500 rounded-full mr-3"></span>
          Performance Test Results
        </h3>

        <div className="space-y-4">
          {performance?.tests?.map((test, index) => (
            <div key={index} className="bg-slate-800/50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-slate-300 font-medium">{test.test}</span>
                <span className={`text-2xl font-bold ${
                  isNeo4j ? 'text-green-400' : 'text-yellow-400'
                }`}>
                  {test.time_ms}ms
                </span>
              </div>
              <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                <div 
                  className={`h-full rounded-full transition-all ${
                    isNeo4j ? 'bg-gradient-to-r from-green-500 to-emerald-500' : 'bg-gradient-to-r from-yellow-500 to-orange-500'
                  }`}
                  style={{ width: `${Math.min((test.time_ms / 100) * 100, 100)}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 bg-indigo-500/10 border border-indigo-500/30 rounded-lg">
          <p className="text-indigo-300 font-semibold">
            Total Test Time: {performance?.total_time_ms}ms
          </p>
        </div>
      </div>

      {/* Comparison */}
      {performance?.comparison && (
        <div className="glass rounded-2xl p-6 border border-slate-700/50">
          <h3 className="text-xl font-semibold text-slate-200 mb-4 flex items-center">
            <span className="w-2 h-2 bg-purple-500 rounded-full mr-3"></span>
            Performance Comparison
          </h3>
          
          <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-6 mb-4">
            <p className="text-purple-300 text-lg font-semibold text-center">
              {performance.comparison.message}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Object.entries(
              performance.comparison.estimated_csv_times || 
              performance.comparison.estimated_neo4j_times || {}
            ).map(([test, time], index) => (
              <div key={index} className="bg-slate-800/50 rounded-lg p-4 text-center">
                <p className="text-slate-400 text-sm mb-2">{test}</p>
                <p className={`text-xl font-bold ${
                  isNeo4j ? 'text-red-400' : 'text-green-400'
                }`}>
                  {time}
                </p>
                <p className="text-slate-500 text-xs mt-1">
                  {isNeo4j ? 'CSV would take' : 'Neo4j would take'}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Speed Comparison Chart */}
      <div className="glass rounded-2xl p-6 border border-slate-700/50">
        <h3 className="text-xl font-semibold text-slate-200 mb-6 flex items-center">
          <span className="w-2 h-2 bg-pink-500 rounded-full mr-3"></span>
          Speed Comparison Visualization
        </h3>

        <div className="space-y-6">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-300">Neo4j Mode</span>
              <span className="text-green-400 font-bold">10-16x Faster</span>
            </div>
            <div className="w-full h-8 bg-slate-700 rounded-lg overflow-hidden">
              <div className="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg flex items-center justify-center text-white font-bold text-sm"
                   style={{ width: '100%' }}>
                Fast ⚡
              </div>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-300">CSV Mode</span>
              <span className="text-yellow-400 font-bold">Baseline</span>
            </div>
            <div className="w-full h-8 bg-slate-700 rounded-lg overflow-hidden">
              <div className="h-full bg-gradient-to-r from-yellow-500 to-orange-500 rounded-lg flex items-center justify-center text-white font-bold text-sm"
                   style={{ width: '10%' }}>
                Slower
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scalability Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass rounded-2xl p-6 border border-slate-700/50">
          <h4 className="text-lg font-semibold text-slate-200 mb-4">CSV Mode</h4>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-slate-400">Max Entities</span>
              <span className="text-yellow-400 font-bold">~10,000</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Storage</span>
              <span className="text-yellow-400 font-bold">In-Memory</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Concurrent Users</span>
              <span className="text-yellow-400 font-bold">1-5</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Best For</span>
              <span className="text-yellow-400 font-bold">Demos</span>
            </div>
          </div>
        </div>

        <div className="glass rounded-2xl p-6 border border-green-500/30">
          <h4 className="text-lg font-semibold text-slate-200 mb-4">Neo4j Mode</h4>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-slate-400">Max Entities</span>
              <span className="text-green-400 font-bold">10,000,000+</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Storage</span>
              <span className="text-green-400 font-bold">Persistent</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Concurrent Users</span>
              <span className="text-green-400 font-bold">100+</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Best For</span>
              <span className="text-green-400 font-bold">Production</span>
            </div>
          </div>
        </div>
      </div>

      {/* Refresh Button */}
      <div className="text-center">
        <button
          onClick={loadData}
          className="px-8 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg hover:shadow-indigo-500/50 transition-all"
        >
          🔄 Run Tests Again
        </button>
      </div>
    </div>
  );
};

export default PerformanceComparison;
