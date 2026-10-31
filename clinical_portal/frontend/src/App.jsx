import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import BackButton from './components/BackButton';
import PortalHome from './pages/PortalHome';
import LandingPage  from './pages/LandingPage';
import UploadPage   from './pages/UploadPage';
import SessionPage  from './pages/SessionPage';
import SubjectsPage from './pages/SubjectsPage';
import SubjectPage  from './pages/SubjectPage';
import StatsPage    from './pages/StatsPage';

function PortalLayout() {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        <div className="topbar"><BackButton /></div>
        <Outlet />
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route element={<PortalLayout />}>
          <Route path="/portal"              element={<PortalHome />} />
          <Route path="/upload"              element={<UploadPage />} />
          <Route path="/sessions/:sessionId" element={<SessionPage />} />
          <Route path="/subjects"            element={<SubjectsPage />} />
          <Route path="/subjects/:subjectId" element={<SubjectPage />} />
          <Route path="/stats"               element={<StatsPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
