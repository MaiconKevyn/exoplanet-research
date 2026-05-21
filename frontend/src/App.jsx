import React, { useMemo } from 'react';
import rankedCandidates from './data/astrobiology_ranked_candidates.json';
import allExoplanets from './data/habitable_zone_calculated.json';
import HabitablePlanetsTable from './components/HabitablePlanetsTable';
import PlanetRadiusDistribution from './components/PlanetRadiusDistribution';
import EvidenceBreakdown from './components/EvidenceBreakdown';
import LiteratureTracePanel from './components/LiteratureTracePanel';

function App() {
  const topCandidates = useMemo(() => rankedCandidates.slice(0, 25), []);
  const insideZoneCandidates = useMemo(
    () => rankedCandidates.filter((planet) => planet.habitable_zone_status === 'inside'),
    []
  );
  const topCandidate = topCandidates[0];

  return (
    <div className="min-h-screen bg-space-dark text-gray-100 font-body relative overflow-hidden">
      <div className="star-background">
        {Array.from({ length: 15 }).map((_, i) => (
          <div key={i} className="star"></div>
        ))}
      </div>

      <header className="bg-space-medium text-white p-4 shadow-lg relative z-10">
        <h1 className="text-4xl font-heading font-bold text-center text-space-star mb-2">Exoplanet Research Dashboard</h1>
        <p className="text-center text-lg text-space-star">Evidence-weighted astrobiology target prioritization</p>
      </header>

      <main className="container mx-auto p-6 relative z-10">
        <section className="mb-8 bg-space-light p-6 rounded-lg shadow-xl">
          <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
            <div>
              <h2 className="text-3xl font-heading font-semibold text-space-star mb-2">Top Follow-up Candidates</h2>
              <p className="text-sm text-gray-300 max-w-3xl">
                Ranked candidates expose sub-scores and caveats. The score prioritizes observation and modeling; it is not a biosignature detection.
              </p>
            </div>
            <div className="text-sm text-gray-300">
              <span className="text-space-star font-semibold">{rankedCandidates.length}</span> scored systems
            </div>
          </div>
          <div className="mt-5">
            <HabitablePlanetsTable data={topCandidates} />
          </div>
        </section>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-8">
          <EvidenceBreakdown candidate={topCandidate} />
          <LiteratureTracePanel />
        </div>

        <section className="mb-8 bg-space-light p-6 rounded-lg shadow-xl">
          <h2 className="text-3xl font-heading font-semibold text-space-star mb-4">Planet Radius Distribution</h2>
          <div className="bg-space-medium p-4 rounded-lg shadow-inner">
            <PlanetRadiusDistribution allExoplanets={allExoplanets} habitableExoplanets={insideZoneCandidates} />
          </div>
        </section>
      </main>

      <footer className="bg-space-medium text-gray-400 p-4 text-center relative z-10">
        <p>Astrobiology candidate ranking with conservative evidence language.</p>
      </footer>
    </div>
  );
}

export default App;
