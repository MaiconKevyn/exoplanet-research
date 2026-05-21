import React from 'react';

const rows = [
  ['HZ position', 'score_hz_position'],
  ['Planet size', 'score_planet_size'],
  ['Stellar context', 'score_stellar_context'],
  ['Data quality', 'score_data_quality'],
  ['Follow-up readiness', 'score_followup_readiness'],
];

const formatScore = (value) => {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return '0.00';
  }
  return Number(value).toFixed(2);
};

function EvidenceBreakdown({ candidate }) {
  if (!candidate) {
    return null;
  }

  return (
    <section className="bg-space-light p-6 rounded-lg shadow-xl">
      <h2 className="text-2xl font-heading font-semibold text-space-star mb-2">Evidence Breakdown</h2>
      <p className="text-sm text-gray-300 mb-5">
        {candidate.pl_name} is the current top-ranked follow-up candidate under the transparent scoring policy.
      </p>
      <div className="space-y-4">
        {rows.map(([label, key]) => {
          const score = Math.max(0, Math.min(1, Number(candidate[key] ?? 0)));
          return (
            <div key={key}>
              <div className="flex items-center justify-between text-sm mb-1">
                <span className="text-gray-200">{label}</span>
                <span className="text-space-star">{formatScore(score)}</span>
              </div>
              <div className="h-2 bg-space-medium rounded">
                <div className="h-2 bg-space-star rounded" style={{ width: `${score * 100}%` }} />
              </div>
            </div>
          );
        })}
      </div>
      <p className="mt-5 text-sm text-gray-300">{candidate.interpretation_caveat}</p>
    </section>
  );
}

export default EvidenceBreakdown;
