import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import * as d3 from 'd3';

const NetworkView = () => {
  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedEntity, setSelectedEntity] = useState(null);
  const svgRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadNetworkGraph();
  }, []);

  useEffect(() => {
    if (graphData && svgRef.current) {
      renderGraph();
    }
  }, [graphData]);

  const loadNetworkGraph = async () => {
    try {
      setLoading(true);
      const response = await api.getNetworkGraph(null, 2);
      setGraphData(response.data);
    } catch (error) {
      console.error('Error loading network:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskCategory) => {
    switch (riskCategory) {
      case 'High': return '#ef4444';
      case 'Medium': return '#f59e0b';
      case 'Low': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getNodeSize = (riskScore) => {
    return 5 + (riskScore * 15);
  };

  const renderGraph = () => {
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = svgRef.current.clientWidth;
    const height = 600;

    const g = svg.append('g');

    // Zoom behavior
    const zoom = d3.zoom()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom);

    // Create force simulation
    const simulation = d3.forceSimulation(graphData.nodes)
      .force('link', d3.forceLink(graphData.edges)
        .id(d => d.id)
        .distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(d => getNodeSize(d.risk_score) + 5));

    // Draw edges
    const link = g.append('g')
      .selectAll('line')
      .data(graphData.edges)
      .enter()
      .append('line')
      .attr('stroke', '#475569')
      .attr('stroke-width', 1)
      .attr('stroke-opacity', 0.6);

    // Draw nodes
    const node = g.append('g')
      .selectAll('circle')
      .data(graphData.nodes)
      .enter()
      .append('circle')
      .attr('r', d => getNodeSize(d.risk_score))
      .attr('fill', d => getRiskColor(d.risk_category))
      .attr('stroke', '#1e293b')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .on('click', (event, d) => {
        setSelectedEntity(d);
      })
      .on('mouseover', function(event, d) {
        d3.select(this)
          .attr('stroke', '#fff')
          .attr('stroke-width', 3);
      })
      .on('mouseout', function(event, d) {
        d3.select(this)
          .attr('stroke', '#1e293b')
          .attr('stroke-width', 2);
      })
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    // Add labels for high-risk nodes
    const label = g.append('g')
      .selectAll('text')
      .data(graphData.nodes.filter(d => d.risk_category === 'High'))
      .enter()
      .append('text')
      .text(d => d.id)
      .attr('font-size', 10)
      .attr('fill', '#e2e8f0')
      .attr('dx', 12)
      .attr('dy', 4);

    // Update positions on tick
    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);

      label
        .attr('x', d => d.x)
        .attr('y', d => d.y);
    });

    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gov-secondary">Loading network graph...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gov-primary">Network Investigation View</h2>
        <p className="text-gov-secondary mt-1">Interactive graph visualization of entity relationships</p>
      </div>

      {/* Legend */}
      <div className="bg-gov-card rounded-lg p-4 border border-gov">
        <div className="flex items-center space-x-8">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-red-500"></div>
            <span className="text-gov-secondary text-sm">High Risk</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-yellow-500"></div>
            <span className="text-gov-secondary text-sm">Medium Risk</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-green-500"></div>
            <span className="text-gov-secondary text-sm">Low Risk</span>
          </div>
          <div className="ml-auto text-gov-secondary text-sm">
            Click nodes to investigate | Drag to reposition | Scroll to zoom
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Network Graph */}
        <div className="lg:col-span-2 bg-gov-card rounded-lg border border-gov overflow-hidden">
          <svg
            ref={svgRef}
            width="100%"
            height="600"
            className="bg-gray-900"
          />
        </div>

        {/* Entity Details Panel */}
        <div className="bg-gov-card rounded-lg p-6 border border-gov">
          <h3 className="text-lg font-semibold text-gov-primary mb-4">Entity Details</h3>
          {selectedEntity ? (
            <div className="space-y-4">
              <div>
                <p className="text-gov-secondary text-sm">Entity ID</p>
                <p className="text-gov-primary font-mono text-sm mt-1">{selectedEntity.id}</p>
              </div>
              <div>
                <p className="text-gov-secondary text-sm">Type</p>
                <p className="text-gov-primary mt-1">{selectedEntity.type}</p>
              </div>
              <div>
                <p className="text-gov-secondary text-sm">Risk Score</p>
                <p className="text-2xl font-bold mt-1" style={{ color: getRiskColor(selectedEntity.risk_category) }}>
                  {(selectedEntity.risk_score * 100).toFixed(1)}%
                </p>
              </div>
              <div>
                <p className="text-gov-secondary text-sm">Risk Category</p>
                <span
                  className={`inline-block px-3 py-1 rounded text-sm font-medium mt-1 risk-${selectedEntity.risk_category.toLowerCase()}`}
                >
                  {selectedEntity.risk_category}
                </span>
              </div>
              {selectedEntity.id.startsWith('COMP_') ? (
                <button
                  onClick={() => navigate(`/entity/${selectedEntity.id}`)}
                  className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition mt-4"
                >
                  Full Investigation →
                </button>
              ) : (
                <div className="mt-4 p-3 bg-gray-800 rounded text-sm text-gov-secondary">
                  Full investigation available for companies only
                </div>
              )}
            </div>
          ) : (
            <p className="text-gov-secondary text-sm">Click on a node to view details</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default NetworkView;
