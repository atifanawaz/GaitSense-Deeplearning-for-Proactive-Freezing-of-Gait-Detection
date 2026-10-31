import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listSubjects } from '../utils/api';

const Icon = ({ d }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d={d} /></svg>
);

export default function PortalHome() {
  const [count, setCount] = useState(null);
  useEffect(() => {
    listSubjects().then(r => setCount(r.data.length)).catch(() => setCount(null));
  }, []);

  const cards = [
    { to: '/upload',   d: 'M12 16V4m0 0l-4 4m4-4l4 4M4 20h16', title: 'New Upload',
      desc: 'Upload an IMU accelerometer CSV, choose the medication state and run the FOG detection pipeline.', cta: 'Start analysis' },
    { to: '/subjects', d: 'M16 20v-2a4 4 0 00-4-4H7a4 4 0 00-4 4v2M9.5 10a4 4 0 100-8 4 4 0 000 8zM21 20v-2a4 4 0 00-3-3.9', title: 'Patients',
      desc: 'Browse subjects, open visit history, progression charts and medication-effect analysis.',
      cta: count != null ? `${count} patient${count !== 1 ? 's' : ''} in database` : 'Open patient list' },
    { to: '/stats',    d: 'M4 20V10m6 10V4m6 16v-7m4 7H2', title: 'Population Stats',
      desc: 'Explore FOG burden distribution, trigger mix and ON/OFF medication differences across all sessions.', cta: 'View statistics' },
  ];

  return (
    <div className="page-content fade-in">
      <div className="page-header">
        <h1>Clinical Portal</h1>
        <p>Choose where to start</p>
      </div>
      <div className="hub-grid">
        {cards.map(c => (
          <Link key={c.to} to={c.to} className="card hub-card">
            <div className="hub-ico"><Icon d={c.d} /></div>
            <h3>{c.title}</h3>
            <p>{c.desc}</p>
            <span className="hub-go">{c.cta} →</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
