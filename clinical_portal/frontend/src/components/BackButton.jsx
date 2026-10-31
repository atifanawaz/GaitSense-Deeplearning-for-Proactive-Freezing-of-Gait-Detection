import { useNavigate, useLocation } from 'react-router-dom';

// Parent page for each portal route; sessions go back in history (they can be opened from several places).
const parentOf = (p) =>
  p === '/portal' ? '/' :
  p.startsWith('/subjects/') ? '/subjects' :
  '/portal';

export default function BackButton() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const label = pathname === '/portal' ? 'Website' : 'Back';
  const go = () => (pathname.startsWith('/sessions/') ? navigate(-1) : navigate(parentOf(pathname)));
  return (
    <button className="back-btn" onClick={go} aria-label="Go back">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 12H5m0 0l6-6m-6 6l6 6" /></svg>
      {label}
    </button>
  );
}
