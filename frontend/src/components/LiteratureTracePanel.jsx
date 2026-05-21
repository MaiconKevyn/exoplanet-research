import React from 'react';

const traces = [
  ['Catling et al. 2018', 'Probabilistic evidence assessment drives sub-scores and caveats.'],
  ['Schwieterman et al. 2018', 'Biosignature plausibility requires environmental context.'],
  ['Krissansen-Totton et al. 2018', 'Chemical disequilibrium is not inferred without atmospheric measurements.'],
  ['NASA EMAC and VPL', 'Platform design separates data, models, outputs, and reusable evidence traces.'],
  ['HWO architecture work', 'Follow-up readiness is exposed for future observatory prioritization.'],
];

function LiteratureTracePanel() {
  return (
    <section className="bg-space-light p-6 rounded-lg shadow-xl">
      <h2 className="text-2xl font-heading font-semibold text-space-star mb-2">Literature Trace</h2>
      <p className="text-sm text-gray-300 mb-5">
        The ranking is tied to modern astrobiology evidence standards and platform patterns.
      </p>
      <div className="space-y-3">
        {traces.map(([source, implication]) => (
          <div key={source} className="border border-space-medium rounded p-3">
            <p className="text-sm font-semibold text-space-star">{source}</p>
            <p className="text-sm text-gray-300">{implication}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default LiteratureTracePanel;
