import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

export default function GraphView({ graphData, predictions, activeDisruption }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!graphData.nodes || graphData.nodes.length === 0) return;

    const width = svgRef.current.clientWidth || 800;
    const height = svgRef.current.clientHeight || 600;

    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('viewBox', [0, 0, width, height]);

    const g = svg.append('g');

    const zoom = d3.zoom()
      .scaleExtent([0.4, 3])
      .on('zoom', (event) => g.attr('transform', event.transform));

    svg.call(zoom);

    const simulation = d3.forceSimulation(graphData.nodes)
      .force('link', d3.forceLink(graphData.edges).id(d => d.id).distance(90))
      .force('charge', d3.forceManyBody().strength(-240))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = g.append('g')
      .selectAll('line')
      .data(graphData.edges)
      .join('line')
      .attr('stroke', '#334155')
      .attr('stroke-width', 2);

    const node = g.append('g')
      .selectAll('circle')
      .data(graphData.nodes)
      .join('circle')
      .attr('r', 12)
      .attr('fill', '#22d3ee')
      .attr('stroke', '#0f172a')
      .attr('stroke-width', 2);

    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
    });

  }, [graphData]);

  return <svg ref={svgRef} className="w-full h-full bg-slate-950" />;
}
