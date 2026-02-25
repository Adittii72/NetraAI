import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import NetworkView from './components/NetworkView';
import EntityProfile from './components/EntityProfile';
import InvestigationReport from './components/InvestigationReport';
import PerformanceComparison from './components/PerformanceComparison';

function Navigation() {
  const location = useLocation();
  const [dbStatus, setDbStatus] = React.useState(null);
  
  React.useEffect(() => {
    // Check database status
    fetch('http://localhost:8000/api/neo4j/status')
      .then(res => res.json())
      .then(data => setDbStatus(data))
      .catch(err => console.error('Failed to get DB status:', err));
  }, []);
  
  const isActive = (path) => location.pathname === path;
  
  return (
    <div className="flex items-center space-x-4">
      <nav className="flex space-x-1">
        <Link 
          to="/" 
          className={`px-6 py-2.5 rounded-lg font-medium transition-all ${
            isActive('/') 
              ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/50' 
              : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
          }`}
        >
          Dashboard
        </Link>
        <Link 
          to="/network" 
          className={`px-6 py-2.5 rounded-lg font-medium transition-all ${
            isActive('/network') 
              ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/50' 
              : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
          }`}
        >
          Network
        </Link>
      </nav>
      
      {/* Database Mode Indicator */}
      {dbStatus && (
        <div className={`flex items-center space-x-2 px-4 py-2 rounded-lg border ${
          dbStatus.status === 'connected' 
            ? 'bg-green-500/10 border-green-500/30 text-green-400' 
            : 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400'
        }`}>
          <div className={`w-2 h-2 rounded-full ${
            dbStatus.status === 'connected' ? 'bg-green-400 animate-pulse' : 'bg-yellow-400'
          }`}></div>
          <span className="text-xs font-semibold">
            {dbStatus.status === 'connected' ? '🚀 Neo4j Mode' : '📊 CSV Mode'}
          </span>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        {/* Animated background */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-pulse"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-pulse" style={{animationDelay: '2s'}}></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-pulse" style={{animationDelay: '4s'}}></div>
        </div>

        {/* Header */}
        <header className="glass-strong sticky top-0 z-50 border-b border-slate-700/50 shadow-2xl">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center space-x-4">
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg blur opacity-75"></div>
                  <div className="relative bg-gradient-to-r from-indigo-500 to-purple-600 p-2 rounded-lg">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                  </div>
                </div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                    NetraAI
                  </h1>
                  <p className="text-xs text-slate-400 font-medium">Investigative Intelligence Platform</p>
                </div>
              </div>
              <Navigation />
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/network" element={<NetworkView />} />
            <Route path="/performance" element={<PerformanceComparison />} />
            <Route path="/entity/:entityId" element={<EntityProfile />} />
            <Route path="/investigation/:entityId" element={<InvestigationReport />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="glass border-t border-slate-700/50 mt-12 relative z-10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-400">
                NetraAI v1.0.0 | Government-Grade Investigative Platform
              </p>
              <div className="flex items-center space-x-4">
                <Link to="/performance" className="text-sm text-slate-400 hover:text-indigo-400 transition">
                  ⚡ Performance Comparison
                </Link>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-500/10 text-green-400 border border-green-500/20">
                  <span className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
                  System Operational
                </span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
