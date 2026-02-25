import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../api/client';

const InvestigationReport = () => {
  const { entityId } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInvestigationReport();
  }, [entityId]);

  const loadInvestigationReport = async () => {
    try {
      setLoading(true);
      
      // Check if it's a company
      if (!entityId.startsWith('COMP_')) {
        setReport(null);
        setLoading(false);
        return;
      }
      
      const response = await api.getInvestigationSummary(entityId);
      setReport(response.data);
    } catch (error) {
      console.error('Error loading investigation report:', error);
      setReport(null);
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

  const getSeverityBadge = (severity) => {
    const colors = {
      High: 'bg-red-900/20 text-red-400',
      Medium: 'bg-yellow-900/20 text-yellow-400',
      Low: 'bg-green-900/20 text-green-400',
    };
    return colors[severity] || 'bg-gray-900/20 text-gray-400';
  };

  const handleExport = () => {
    const reportText = generateReportText();
    const blob = new Blob([reportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `investigation_report_${entityId}_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const generateReportText = () => {
    if (!report) return '';

    return `
═══════════════════════════════════════════════════════════════
NETRAAI INVESTIGATION SUMMARY REPORT
Government-Grade Investigative Intelligence Platform
═══════════════════════════════════════════════════════════════

REPORT GENERATED: ${new Date().toLocaleString()}
CLASSIFICATION: CONFIDENTIAL

───────────────────────────────────────────────────────────────
ENTITY INFORMATION
───────────────────────────────────────────────────────────────

Entity ID:       ${report.entity_id}
Entity Type:     ${report.entity_type}
Risk Score:      ${(report.risk_score * 100).toFixed(2)}%
Risk Category:   ${report.risk_category}

───────────────────────────────────────────────────────────────
RISK ASSESSMENT
───────────────────────────────────────────────────────────────

${report.risk_indicators.map((indicator, i) => `
${i + 1}. ${indicator.indicator} [${indicator.severity}]
   ${indicator.description}
`).join('\n')}

───────────────────────────────────────────────────────────────
KEY FINDINGS
───────────────────────────────────────────────────────────────

${report.key_findings.map((finding, i) => `${i + 1}. ${finding}`).join('\n')}

───────────────────────────────────────────────────────────────
CONNECTED SUSPICIOUS ENTITIES
───────────────────────────────────────────────────────────────

${report.connected_suspicious_entities.length > 0 
  ? report.connected_suspicious_entities.map((e, i) => `${i + 1}. ${e}`).join('\n')
  : 'No connected suspicious entities identified.'}

───────────────────────────────────────────────────────────────
RECOMMENDATION
───────────────────────────────────────────────────────────────

${report.recommendation}

───────────────────────────────────────────────────────────────
INVESTIGATOR NOTES
───────────────────────────────────────────────────────────────

[Space for manual notes]




═══════════════════════════════════════════════════════════════
END OF REPORT
═══════════════════════════════════════════════════════════════

This report is generated by NetraAI v1.0.0
For official use only | Confidential
    `.trim();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gov-secondary">Generating investigation report...</div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="text-center py-12">
        <p className="text-gov-secondary mb-4">
          {entityId.startsWith('COMP_') 
            ? 'Unable to generate report' 
            : 'Investigation reports are only available for companies'}
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
            onClick={() => navigate(`/entity/${entityId}`)}
            className="text-blue-400 hover:text-blue-300 text-sm mb-2"
          >
            ← Back to Entity Profile
          </button>
          <h2 className="text-3xl font-bold text-gov-primary">Investigation Summary Report</h2>
          <p className="text-gov-secondary mt-1">Confidential | For Official Use Only</p>
        </div>
        <button
          onClick={handleExport}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition flex items-center space-x-2"
        >
          <span>📄</span>
          <span>Export Report</span>
        </button>
      </div>

      {/* Report Container */}
      <div className="bg-gov-card rounded-lg border border-gov overflow-hidden">
        {/* Report Header */}
        <div className="bg-gray-900 border-b border-gov p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold text-gov-primary">NetraAI Investigation Report</h3>
              <p className="text-gov-secondary text-sm mt-1">
                Generated: {new Date().toLocaleString()}
              </p>
            </div>
            <div className="text-right">
              <p className="text-gov-secondary text-sm">Classification</p>
              <p className="text-red-400 font-semibold mt-1">CONFIDENTIAL</p>
            </div>
          </div>
        </div>

        {/* Entity Information */}
        <div className="p-6 border-b border-gov">
          <h4 className="text-lg font-semibold text-gov-primary mb-4">Entity Information</h4>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-gov-secondary text-sm">Entity ID</p>
              <p className="text-gov-primary font-mono mt-1">{report.entity_id}</p>
            </div>
            <div>
              <p className="text-gov-secondary text-sm">Entity Type</p>
              <p className="text-gov-primary mt-1">{report.entity_type}</p>
            </div>
            <div>
              <p className="text-gov-secondary text-sm">Risk Score</p>
              <p className="text-3xl font-bold mt-1" style={{ color: getRiskColor(report.risk_category) }}>
                {(report.risk_score * 100).toFixed(2)}%
              </p>
            </div>
            <div>
              <p className="text-gov-secondary text-sm">Risk Category</p>
              <span
                className={`inline-block px-3 py-1 rounded text-sm font-medium mt-1 risk-${report.risk_category.toLowerCase()}`}
              >
                {report.risk_category}
              </span>
            </div>
          </div>
        </div>

        {/* Risk Indicators */}
        <div className="p-6 border-b border-gov">
          <h4 className="text-lg font-semibold text-gov-primary mb-4">Risk Indicators</h4>
          <div className="space-y-3">
            {report.risk_indicators.map((indicator, index) => (
              <div key={index} className="bg-gray-800 rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getSeverityBadge(indicator.severity)}`}>
                        {indicator.severity}
                      </span>
                      <h5 className="font-semibold text-gov-primary">{indicator.indicator}</h5>
                    </div>
                    <p className="text-gov-secondary text-sm mt-2">{indicator.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Key Findings */}
        <div className="p-6 border-b border-gov">
          <h4 className="text-lg font-semibold text-gov-primary mb-4">Key Findings</h4>
          <ul className="space-y-2">
            {report.key_findings.map((finding, index) => (
              <li key={index} className="flex items-start space-x-3">
                <span className="text-blue-400 font-bold">{index + 1}.</span>
                <span className="text-gov-primary">{finding}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Connected Suspicious Entities */}
        <div className="p-6 border-b border-gov">
          <h4 className="text-lg font-semibold text-gov-primary mb-4">Connected Suspicious Entities</h4>
          {report.connected_suspicious_entities.length === 0 ? (
            <p className="text-gov-secondary">No connected suspicious entities identified.</p>
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {report.connected_suspicious_entities.map((entity, index) => (
                <div key={index} className="bg-gray-800 rounded p-3 flex items-center justify-between">
                  <span className="text-gov-primary font-mono text-sm">{entity}</span>
                  <button
                    onClick={() => navigate(`/entity/${entity}`)}
                    className="text-blue-400 hover:text-blue-300 text-sm"
                  >
                    View →
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recommendation */}
        <div className="p-6 bg-gray-900">
          <h4 className="text-lg font-semibold text-gov-primary mb-4">Recommendation</h4>
          <div className={`p-4 rounded-lg ${
            report.risk_category === 'High' ? 'bg-red-900/20 border border-red-800' :
            report.risk_category === 'Medium' ? 'bg-yellow-900/20 border border-yellow-800' :
            'bg-green-900/20 border border-green-800'
          }`}>
            <p className="text-gov-primary leading-relaxed">{report.recommendation}</p>
          </div>
        </div>
      </div>

      {/* Footer Note */}
      <div className="bg-gov-card rounded-lg p-4 border border-gov">
        <p className="text-gov-secondary text-sm text-center">
          This report is generated by NetraAI v1.0.0 | For official use only | Confidential
        </p>
      </div>
    </div>
  );
};

export default InvestigationReport;
