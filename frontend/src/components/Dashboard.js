import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRisk, setSelectedRisk] = useState('High');
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboardData();
  }, []);

  useEffect(() => {
    loadCompanies(selectedRisk);
  }, [selectedRisk]);

  const loadDashboardData = async () => {
    try {
      const response = await api.getDashboardStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  const loadCompanies = async (riskCategory) => {
    try {
      setLoading(true);
      const response = await api.getCompanies(riskCategory, 50);
      setCompanies(response.data);
    } catch (error) {
      console.error('Error loading companies:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (category) => {
    switch (category) {
      case 'High': return '#ef4444';
      case 'Medium': return '#f59e0b';
      case 'Low': return '#10b981';
      default: return '#6b7280';
    }
  };

  const riskDistributionData = stats ? [
    { name: 'High Risk', value: stats.risk_distribution.High || 0, color: '#ef4444' },
    { name: 'Medium Risk', value: stats.risk_distribution.Medium || 0, color: '#f59e0b' },
    { name: 'Low Risk', value: stats.risk_distribution.Low || 0, color: '#10b981' },
  ] : [];

  if (!stats) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-400 text-lg">Loading intelligence data...</p>
          <p className="text-slate-500 text-sm">⏳ First load may take 30-60 seconds (free tier waking up)</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 fade-in-up">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-4xl font-bold bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
          Investigation Dashboard
        </h2>
        <p className="text-slate-400 text-lg">Proactive corruption detection in public procurement</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Entities"
          value={stats.total_entities.toLocaleString()}
          subtitle="Companies & Directors"
          icon="📊"
          gradient="from-blue-500 to-cyan-500"
          delay="0s"
        />
        <StatCard
          title="High Risk Entities"
          value={stats.high_risk_count}
          subtitle="Immediate attention required"
          icon="⚠️"
          gradient="from-red-500 to-pink-500"
          delay="0.1s"
          pulse
        />
        <StatCard
          title="Fraud Clusters"
          value={stats.fraud_cluster_count}
          subtitle="Detected collusion networks"
          icon="🕸️"
          gradient="from-orange-500 to-yellow-500"
          delay="0.2s"
        />
        <StatCard
          title="Total Contract Value"
          value={`₹${(stats.total_contract_value / 1000000).toFixed(1)}M`}
          subtitle={`${stats.total_tenders} tenders`}
          icon="💰"
          gradient="from-green-500 to-emerald-500"
          delay="0.3s"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Distribution */}
        <div className="glass rounded-2xl p-6 card-hover border border-slate-700/50">
          <h3 className="text-xl font-semibold text-slate-200 mb-6 flex items-center">
            <span className="w-2 h-2 bg-indigo-500 rounded-full mr-3"></span>
            Risk Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={riskDistributionData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {riskDistributionData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(30, 41, 59, 0.95)', 
                  border: '1px solid rgba(148, 163, 184, 0.2)',
                  borderRadius: '8px',
                  color: '#e2e8f0'
                }} 
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Quick Stats */}
        <div className="glass rounded-2xl p-6 card-hover border border-slate-700/50">
          <h3 className="text-xl font-semibold text-slate-200 mb-6 flex items-center">
            <span className="w-2 h-2 bg-purple-500 rounded-full mr-3"></span>
            System Overview
          </h3>
          <div className="space-y-4">
            <QuickStat label="Detection Rate" value="85.3%" color="text-green-400" />
            <QuickStat label="Active Investigations" value={stats.high_risk_count} color="text-yellow-400" />
            <QuickStat label="Patterns Detected" value="6 Types" color="text-blue-400" />
            <QuickStat label="Network Density" value="Sparse" color="text-purple-400" />
          </div>
        </div>
      </div>

      {/* Entity Risk Assessment Table */}
      <div className="glass rounded-2xl p-6 border border-slate-700/50">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-semibold text-slate-200 flex items-center">
            <span className="w-2 h-2 bg-pink-500 rounded-full mr-3"></span>
            Entity Risk Assessment
          </h3>
          <div className="flex space-x-2">
            {['High', 'Medium', 'Low'].map((risk) => (
              <button
                key={risk}
                onClick={() => setSelectedRisk(risk)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  selectedRisk === risk
                    ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/50'
                    : 'bg-slate-700/50 text-slate-300 hover:bg-slate-700'
                }`}
              >
                {risk} Risk
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="skeleton h-16 rounded-lg"></div>
            ))}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left py-4 px-4 text-slate-400 font-medium text-sm">Company ID</th>
                  <th className="text-left py-4 px-4 text-slate-400 font-medium text-sm">Name</th>
                  <th className="text-left py-4 px-4 text-slate-400 font-medium text-sm">Industry</th>
                  <th className="text-left py-4 px-4 text-slate-400 font-medium text-sm">Risk Score</th>
                  <th className="text-left py-4 px-4 text-slate-400 font-medium text-sm">Category</th>
                  <th className="text-left py-4 px-4 text-slate-400 font-medium text-sm">Actions</th>
                </tr>
              </thead>
              <tbody>
                {companies.slice(0, 15).map((company, index) => (
                  <tr 
                    key={company.company_id} 
                    className="border-b border-slate-800 table-row-hover"
                    style={{ animationDelay: `${index * 0.05}s` }}
                  >
                    <td className="py-4 px-4">
                      <span className="font-mono text-sm text-slate-300 bg-slate-800 px-2 py-1 rounded">
                        {company.company_id}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-slate-200 font-medium">{company.name}</td>
                    <td className="py-4 px-4 text-slate-400 text-sm">{company.industry_type}</td>
                    <td className="py-4 px-4">
                      <div className="flex items-center space-x-2">
                        <div className="w-24 h-2 bg-slate-700 rounded-full overflow-hidden">
                          <div 
                            className="h-full rounded-full transition-all"
                            style={{ 
                              width: `${company.risk_score * 100}%`,
                              background: `linear-gradient(90deg, ${getRiskColor(company.risk_category)}, ${getRiskColor(company.risk_category)}dd)`
                            }}
                          ></div>
                        </div>
                        <span className="font-semibold text-sm" style={{ color: getRiskColor(company.risk_category) }}>
                          {(company.risk_score * 100).toFixed(1)}%
                        </span>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <span className={`badge risk-${company.risk_category.toLowerCase()}`}>
                        {company.risk_category}
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <button
                        onClick={() => navigate(`/entity/${company.company_id}`)}
                        className="px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-sm font-medium rounded-lg hover:shadow-lg hover:shadow-indigo-500/50 transition-all"
                      >
                        Investigate →
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

const StatCard = ({ title, value, subtitle, icon, gradient, delay, pulse }) => (
  <div 
    className={`glass rounded-2xl p-6 card-hover border border-slate-700/50 ${pulse ? 'pulse-glow' : ''}`}
    style={{ animationDelay: delay }}
  >
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <p className="text-slate-400 text-sm font-medium mb-2">{title}</p>
        <p className={`text-3xl font-bold bg-gradient-to-r ${gradient} bg-clip-text text-transparent mb-1`}>
          {value}
        </p>
        <p className="text-slate-500 text-xs">{subtitle}</p>
      </div>
      <div className={`text-4xl bg-gradient-to-r ${gradient} p-3 rounded-xl`}>
        {icon}
      </div>
    </div>
  </div>
);

const QuickStat = ({ label, value, color }) => (
  <div className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg">
    <span className="text-slate-400 text-sm">{label}</span>
    <span className={`font-semibold ${color}`}>{value}</span>
  </div>
);

export default Dashboard;
