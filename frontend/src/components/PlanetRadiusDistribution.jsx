import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function PlanetRadiusDistribution({ allExoplanets, habitableExoplanets }) {
  const allRadii = allExoplanets.map(p => p.pl_rade).filter(r => r > 0 && r <= 10);
  const habitableRadii = habitableExoplanets.map(p => p.pl_rade).filter(r => r > 0 && r <= 10);

  const bins = Array.from({ length: 10 }, (_, i) => i + 1);

  const data = bins.map(bin => {
    const allCount = allRadii.filter(r => r > (bin - 1) && r <= bin).length;
    const habitableCount = habitableRadii.filter(r => r > (bin - 1) && r <= bin).length;
    return {
      name: `${bin - 1}-${bin} Re`,
      'All Exoplanets': allCount,
      'Inside HZ': habitableCount,
    };
  });

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={data}
        margin={{
          top: 20, right: 30, left: 20, bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#4A4A7A" />
        <XAxis dataKey="name" stroke="#E0E0E0" label={{ value: 'Planet Radius (Earth Radii)', position: 'insideBottom', offset: 0, fill: '#E0E0E0' }} />
        <YAxis stroke="#E0E0E0" label={{ value: 'Number of Exoplanets', angle: -90, position: 'insideLeft', fill: '#E0E0E0' }} />
        <Tooltip
          cursor={{ fill: 'rgba(255,255,255,0.1)' }}
          contentStyle={{ backgroundColor: '#1A1A4A', border: 'none', borderRadius: '5px' }}
          labelStyle={{ color: '#E0E0E0' }}
          itemStyle={{ color: '#E0E0E0' }}
        />
        <Legend wrapperStyle={{ color: '#E0E0E0' }} />
        <Bar dataKey="All Exoplanets" fill="#8884d8" />
        <Bar dataKey="Inside HZ" fill="#82ca9d" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default PlanetRadiusDistribution;
