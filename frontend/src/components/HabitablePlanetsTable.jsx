import React from 'react';

const formatNumber = (value, digits = 2) => {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return 'n/a';
  }
  return Number(value).toFixed(digits);
};

function HabitablePlanetsTable({ data }) {
  return (
    <div className="overflow-x-auto bg-space-medium rounded-lg shadow-lg">
      <table className="min-w-full leading-normal">
        <thead>
          <tr>
            <th className="px-5 py-3 border-b-2 border-space-light bg-space-medium text-left text-xs font-semibold text-space-star uppercase tracking-wider">
              Planet
            </th>
            <th className="px-5 py-3 border-b-2 border-space-light bg-space-medium text-left text-xs font-semibold text-space-star uppercase tracking-wider">
              Host
            </th>
            <th className="px-5 py-3 border-b-2 border-space-light bg-space-medium text-left text-xs font-semibold text-space-star uppercase tracking-wider">
              Total Score
            </th>
            <th className="px-5 py-3 border-b-2 border-space-light bg-space-medium text-left text-xs font-semibold text-space-star uppercase tracking-wider">
              HZ
            </th>
            <th className="px-5 py-3 border-b-2 border-space-light bg-space-medium text-left text-xs font-semibold text-space-star uppercase tracking-wider">
              Size
            </th>
            <th className="px-5 py-3 border-b-2 border-space-light bg-space-medium text-left text-xs font-semibold text-space-star uppercase tracking-wider">
              Data
            </th>
            <th className="px-5 py-3 border-b-2 border-space-light bg-space-medium text-left text-xs font-semibold text-space-star uppercase tracking-wider">
              Confidence
            </th>
            <th className="px-5 py-3 border-b-2 border-space-light bg-space-medium text-left text-xs font-semibold text-space-star uppercase tracking-wider">
              Caveat
            </th>
          </tr>
        </thead>
        <tbody>
          {data.map((planet, index) => (
            <tr key={index} className="hover:bg-space-light transition-colors duration-200">
              <td className="px-5 py-5 border-b border-space-light bg-space-medium text-sm">
                <p className="text-gray-200 whitespace-no-wrap">{planet.pl_name}</p>
              </td>
              <td className="px-5 py-5 border-b border-space-light bg-space-medium text-sm">
                <p className="text-gray-200 whitespace-no-wrap">{planet.hostname}</p>
              </td>
              <td className="px-5 py-5 border-b border-space-light bg-space-medium text-sm">
                <p className="text-gray-200 whitespace-no-wrap">{formatNumber(planet.score_total, 3)}</p>
              </td>
              <td className="px-5 py-5 border-b border-space-light bg-space-medium text-sm">
                <p className="text-gray-200 whitespace-no-wrap">{formatNumber(planet.score_hz_position, 2)}</p>
              </td>
              <td className="px-5 py-5 border-b border-space-light bg-space-medium text-sm">
                <p className="text-gray-200 whitespace-no-wrap">{formatNumber(planet.score_planet_size, 2)}</p>
              </td>
              <td className="px-5 py-5 border-b border-space-light bg-space-medium text-sm">
                <p className="text-gray-200 whitespace-no-wrap">{formatNumber(planet.score_data_quality, 2)}</p>
              </td>
              <td className="px-5 py-5 border-b border-space-light bg-space-medium text-sm">
                <p className="text-gray-200 whitespace-no-wrap">{planet.evidence_confidence}</p>
              </td>
              <td className="px-5 py-5 border-b border-space-light bg-space-medium text-sm max-w-md">
                <p className="text-gray-200">{planet.interpretation_caveat}</p>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HabitablePlanetsTable;
