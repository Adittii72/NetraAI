import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../api/client';

const EntityProfile = () => {
  const { entityId } = useParams();
  const navigate = useNavigate();
  const [entity, setEntity] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadEntityDetail();
  }, [entityId]);

  const loadEntityDetail = async () => {
    try {
      setLoading(true);
      
      // Check if it's a company
      if (!entityId.startsWith('COMP_')) {
        setEntity(null);
        setLoading(false);
        return;
      }
      
      const response = await api.getCompanyDetail(entityId);
      setEntity(response.data);
    } catch (error) {
      console.error('Error loading entity:', error);
      setEntity(null);
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

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'High': return 'text-red-400 bg-red-900/20';
      case 'Medium': return 'text-yellow-400 bg-yellow-900/20';
      case 'Low': return 'text-green-400 bg-green-900/20';
      default: return 'text-gray-400 bg-gray-900/20';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gov-secondary">Loading entity profile...</div>
      </div>
    );
  }

  if (!entity) {
    return (
      <div className="text-center py-12">
        <p className="text-gov-secondary mb-4">
          {entityId.startsWith('COMP_') 
            ? 'Company not found' 
            : 'Investigation profiles are only available for companies'}
        </p>
        <button
          onClick={() => navigate('/')}
          className="text-blue-400 hover:text-blue-300"
        >
          ← Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <button
            onClick={() => navigate('/')}
            className="text-blue-400 hover:text-blue-300 text-sm mb-2"
          >
            ← Back to Dashboard
          </button>
          <h2 className="text-3xl font-bold text-gov-primary">Entity Profile</h2>
          <p className="text-gov-secondary mt-1">{entity.entity_id}</p>
        </div>
        <button
          onClick={() => navigate(`/investigation/${entityId}`)}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition"
        >
          Generate Investigation Report
        </button>
      </div>

      {/* Risk Score Card */}
      <div className="bg-gov-card rounded-lg p-6 border border-gov">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gov-secondary mb-2">Risk Assessment</h3>
            <div className="flex items-baseline space-x-4">
              <span className="text-5xl font-bold" style={{ color: getRiskColor(entity.risk_category) }}>
                {(entity.risk_score * 100).toFixed(1)}%
              </span>
              <span
                className={`px-3 py-1 rounded text-sm font-medium risk-${entity.risk_category.toLowerCase()}`}
              >
                {entity.risk_category} Risk
              </span>
            </div>
          </div>
          <div className="text-right">
            <p className="text-gov-secondary text-sm">Confidence Score</p>
            <p className="text-2xl font-bold text-gov-primary mt-1">
              {/* Confidence score would come from API */}
              85%
            </p>
          </div>
        </div>
      </div>

      {/* Risk Indicators */}
      <div className="bg-gov-card rounded-lg p-6 border border-gov">
        <h3 className="text-xl font-semibold text-gov-primary mb-4">Risk Indicators</h3>
        {entity.risk_indicators.length === 0 ? (
          <p className="text-gov-secondary">No significant risk indicators detected</p>
        ) : (
          <div className="space-y-3">
            {entity.risk_indicators.map((indicator, index) => (
              <div
                key={index}
                className="flex items-start space-x-4 p-4 bg-gray-800 rounded-lg"
              >
                <div className={`px-3 py-1 rounded text-xs font-medium ${getSeverityColor(indicator.severity)}`}>
                  {indicator.severity}
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-gov-primary">{indicator.indicator}</p>
                  <p className="text-sm text-gov-secondary mt-1">{indicator.description}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Tender History */}
      {entity.tender_history && entity.tender_history.length > 0 && (
        <div className="bg-gov-card rounded-lg p-6 border border-gov">
          <h3 className="text-xl font-semibold text-gov-primary mb-4">Tender History</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gov">
                  <th className="text-left py-3 px-4 text-gov-secondary font-medium">Tender ID</th>
                  <th className="text-left py-3 px-4 text-gov-secondary font-medium">Year</th>
                  <th className="text-left py-3 px-4 text-gov-secondary font-medium">Contract Value</th>
                </tr>
              </thead>
              <tbody>
                {entity.tender_history.map((tender) => (
                  <tr key={tender.tender_id} className="border-b border-gov">
                    <td className="py-3 px-4 text-gov-primary font-mono text-sm">{tender.tender_id}</td>
                    <td className="py-3 px-4 text-gov-primary">{tender.year}</td>
                    <td className="py-3 px-4 text-gov-primary font-semibold">
                      ₹{tender.contract_value.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Connected Entities */}
      <div className="bg-gov-card rounded-lg p-6 border border-gov">
        <h3 className="text-xl font-semibold text-gov-primary mb-4">Connected Entities</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {entity.connected_entities.slice(0, 10).map((conn, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-800 rounded">
              <div>
                <p className="text-gov-primary font-mono text-sm">{conn.entity_id}</p>
                <p className="text-gov-secondary text-xs mt-1">{conn.relationship_type}</p>
              </div>
              <button
                onClick={() => navigate(`/entity/${conn.entity_id}`)}
                className="text-blue-400 hover:text-blue-300 text-sm"
              >
                View →
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EntityProfile;
