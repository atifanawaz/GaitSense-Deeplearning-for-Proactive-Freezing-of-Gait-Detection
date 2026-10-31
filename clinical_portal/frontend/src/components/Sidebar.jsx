import { NavLink } from 'react-router-dom';

const Icon = ({ d }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d={d} /></svg>
);

const navItems = [
  { to: '/portal',   d: 'M3 11l9-8 9 8v9a1 1 0 01-1 1h-5v-6H9v6H4a1 1 0 01-1-1z', label: 'Dashboard' },
  { to: '/upload',   d: 'M12 16V4m0 0l-4 4m4-4l4 4M4 20h16', label: 'New Upload' },
  { to: '/subjects', d: 'M16 20v-2a4 4 0 00-4-4H7a4 4 0 00-4 4v2M9.5 10a4 4 0 100-8 4 4 0 000 8zM21 20v-2a4 4 0 00-3-3.9', label: 'Patients' },
  { to: '/stats',    d: 'M4 20V10m6 10V4m6 16v-7m4 7H2',     label: 'Population Stats' },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <NavLink to="/" className="logo-mark" style={{ textDecoration: 'none' }}>
          <div className="logo-icon"><Icon d="M3 12h4l3-8 4 16 3-8h4" /></div>
          <div>
            <div className="logo-text">GaitSense</div>
            <div className="logo-sub">Clinical Portal</div>
          </div>
        </NavLink>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Navigation</div>
        {navItems.map(item => (
          <NavLink key={item.to} to={item.to}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <span className="nav-icon"><Icon d={item.d} /></span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      <NavLink to="/" className="sidebar-back">← Back to website</NavLink>
      <div className="sidebar-footer">
        GaitSense v1.0<br />
        <span style={{ color: 'var(--accent-light)' }}>●</span> Clinical Research Tool
      </div>
    </aside>
  );
}
