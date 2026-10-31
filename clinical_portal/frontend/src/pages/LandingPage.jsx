import { Link } from 'react-router-dom';
import '../styles/landing.css';

export default function LandingPage() {
  return (

<div className="lp">
  <header className="lp-nav"><div className="lp-capsule">
    <Link to="/" className="lp-logo"><svg className="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M3 12h4l3-8 4 16 3-8h4"/></svg></Link>
    <nav className="lp-links"><Link to="/">Home</Link><a href="#features">Features</a><a href="#workflow">Workflow</a><a href="#technology">Technology</a></nav>
    <Link to="/portal" className="lp-white">Open Portal</Link>
  </div></header>

  <section className="lp-hero2">
    <i className="st st1"></i><i className="st st2"></i><i className="st st3"></i><i className="st st4"></i><i className="st st5"></i><i className="st st6"></i><i className="st st7"></i>
    <div className="lp-wrap hero-in">
      <span className="lp-pill2"><svg className="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/></svg> New: AI Freezing of Gait detection is live</span>
      <h1>Detect Freezing of Gait Smarter, Analyze Faster Thanks to AI</h1>
      <p className="lead2">Upload a wearable sensor recording and let AI detect every episode, classify its trigger and track progression across visits, all in one clinical workflow.</p>
      <div className="lp-cta"><Link to="/portal" className="lp-btn pri lg">Get Started <svg className="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M7 17L17 7M8 7h9v9"/></svg></Link><a href="#features" className="lp-btn gho lg">Learn More</a></div>
      <div className="lp-orbzone"><div className="rings"></div><div className="beam"></div><div className="lp-orb"><span><svg className="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M3 12h4l3-8 4 16 3-8h4"/></svg></span></div></div>
      <div className="lp-stack2">
        <div className="vline"></div>
        <div className="lp-chip2"><svg className="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8zM14 3v5h5"/></svg> Upload CSV</div>
        <div className="lp-trio"><span><i className="dot d1"></i>Hesitation</span><span><i className="dot d2"></i>Turn</span><span><i className="dot d3"></i>Walking</span></div>
        <div className="vline"></div><div className="lp-plus">+</div><div className="vline"></div>
        <div className="lp-task">
          <h5>You uploaded, we analyzed.</h5>
          <small>Detected episodes · sample output</small>
          <div className="tk"><i className="okc"></i><span>Start Hesitation</span><div className="tags"><em className="r">2.4 s</em><em className="o">Med ON</em></div><span className="dt">Visit 4</span></div>
          <div className="tk f1"><i className="okc"></i><span>Turn</span><div className="tags"><em className="r">1.8 s</em><em className="o">Med OFF</em></div><span className="dt">Visit 3</span></div>
          <div className="tk f2"><i className="okc"></i><span>Walking</span><div className="tags"><em className="r">3.1 s</em><em className="o">Med ON</em></div><span className="dt">Visit 2</span></div>
        </div>
        <div className="fp p1"><i className="fi y">?</i>Uncertain</div>
        <div className="fp p2"><i className="fi b">◔</i>Analyzing</div>
        <div className="fp p3"><i className="fi r">✕</i>Artifact</div>
        <div className="fp p4"><i className="fi g">✓</i>Confirmed</div>
        <div className="cur c1">Clinician</div><div className="cur c2">AI model</div>
      </div>
    </div>
  </section>

  <section className="lp-wrap lp-tech" id="technology">
    <p>Built for <b>Parkinson’s research</b>, combining wearable sensing, deep learning and privacy-aware training in one <b>clinical workflow</b>.</p>
    <div className="lp-chips"><div className="lp-chip">Federated Learning</div><div className="lp-chip">IMU Sensors</div><div className="lp-chip">CNN + BiLSTM + FiLM</div><div className="lp-chip">FastAPI</div><div className="lp-chip">React</div><div className="lp-chip">Plotly</div></div>
  </section>

  <section className="lp-wrap lp-sec" id="features">
    <h2>Learn About the Most Important Features of Our Platform</h2>
    <p className="sub">Everything a clinician or researcher needs to go from a raw recording to an interpretable result.</p>
    <div className="lp-bento">
      <div className="lp-card wide">
        <div className="lp-viz">
          <svg viewBox="0 0 120 120" width="130" height="130" fill="none" strokeWidth="16"><g transform="rotate(-90 60 60)"><circle cx="60" cy="60" r="44" stroke="#f87171" strokeDasharray="110.6 276.5"/><circle cx="60" cy="60" r="44" stroke="#5aa2ff" strokeDasharray="96.8 276.5" strokeDashoffset="-110.6"/><circle cx="60" cy="60" r="44" stroke="#34d399" strokeDasharray="69.1 276.5" strokeDashoffset="-207.4"/></g></svg>
          <div className="lp-legend"><span><i className="dot d1"></i>Start Hesitation</span><span><i className="dot d2"></i>Turn</span><span><i className="dot d3"></i>Walking</span></div>
        </div>
        <h3>Trigger Classification</h3><p>Each episode is labelled as start hesitation, turning or walking, with per-class confidence so targeted rehabilitation can follow the trigger.</p>
      </div>
      <div className="lp-card">
        <div className="lp-viz"><svg viewBox="0 0 220 90" width="100%" height="90" fill="none" strokeLinecap="round" strokeWidth="3"><path d="M4 70h40" stroke="#4a3a5a"/><path d="M48 70h38" stroke="#f87171"/><path d="M90 70h50" stroke="#4a3a5a"/><path d="M144 70h26" stroke="#5aa2ff"/><path d="M174 70h42" stroke="#4a3a5a"/><path className="draw" d="M4 40 C30 40 40 12 66 14 S100 44 130 40 S160 10 190 18 S212 38 216 36" stroke="#d58bff" strokeWidth="2"/></svg></div>
        <h3>Automatic FOG Detection</h3><p>Sliding-window inference flags every freezing episode with start time, duration and confidence.</p>
      </div>
      <div className="lp-card">
        <div className="lp-viz"><svg viewBox="0 0 160 100" width="100%" height="100"><rect x="30" y="30" width="38" height="60" rx="8" fill="#34d399" opacity=".85"/><rect x="92" y="8" width="38" height="82" rx="8" fill="#f87171" opacity=".85"/></svg></div>
        <h3>Medication Effect</h3><p>Compare ON and OFF recordings to see how FOG burden shifts with medication.</p>
      </div>
      <div className="lp-card">
        <div className="lp-viz"><svg viewBox="0 0 220 90" width="100%" height="90" fill="none"><path className="draw" d="M6 74 L52 58 L98 62 L144 34 L214 14" stroke="#d58bff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/><circle cx="6" cy="74" r="4" fill="#d58bff"/><circle cx="52" cy="58" r="4" fill="#d58bff"/><circle cx="98" cy="62" r="4" fill="#d58bff"/><circle cx="144" cy="34" r="4" fill="#d58bff"/><circle cx="214" cy="14" r="4" fill="#d58bff"/></svg></div>
        <h3>Visit Progression</h3><p>Track FOG burden and trigger mix for each patient over time.</p>
      </div>
      <div className="lp-card">
        <div className="lp-viz"><div className="lp-pillrow"><span className="pc">✓ Confirmed</span><span className="pu">? Uncertain</span><span className="pa">✕ Artifact</span></div></div>
        <h3>Clinician Annotation</h3><p>Review each episode and mark it so the record reflects clinical judgement.</p>
      </div>
    </div>
  </section>

  <section className="lp-wrap lp-sec" id="workflow">
    <h2>From Raw Signal to Clinical Insight in Four Steps</h2>
    <p className="sub">Drop in a recording, tell us the medication state, and the pipeline does the rest.</p>
    <div className="lp-flow">
      <div className="lp-stack">
        <div className="lp-glass s1">Upload<b>recording.csv</b></div>
        <div className="lp-glass s2">Analysis<b>FOG detected</b></div>
        <div className="lp-glass s3">Result<b>Report ready</b></div>
      </div>
      <div>
        <div className="lp-steps">
          <div className="lp-step"><div className="n">1</div><h4>Upload CSV</h4><p>Accelerometer data with AccV, AccML and AccAP columns.</p></div>
          <div className="lp-step"><div className="n">2</div><h4>Select status</h4><p>Mark the recording as ON or OFF medication.</p></div>
          <div className="lp-step"><div className="n">3</div><h4>AI analysis</h4><p>Episodes detected and triggers classified.</p></div>
          <div className="lp-step"><div className="n">4</div><h4>View results</h4><p>Metrics, progression and a downloadable report.</p></div>
        </div>
      </div>
    </div>
    <div className="lp-bento">
      <div className="lp-card"><h3><svg className="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M12 16V4m0 0l-4 4m4-4l4 4M4 20h16"/></svg> Fast intake</h3><p>Drag-and-drop upload with live pipeline progress.</p></div>
      <div className="lp-card"><h3><svg className="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/></svg> Privacy-aware</h3><p>Built on federated learning research for sensitive health data.</p></div>
      <div className="lp-card"><h3><svg className="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8zM14 3v5h5"/></svg> Reports and export</h3><p>Download a PDF report or export episodes as CSV.</p></div>
    </div>
  </section>

  <section className="lp-wrap lp-sec">
    <h2>A Complete Pipeline, Ready to Use</h2>
    <p className="sub">Signal in, clinical insight out, with every stage of the stack working together.</p>
    <div className="lp-arc">
      <div className="ring"></div><div className="ring r2"></div><div className="core"><svg className="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M3 12h4l3-8 4 16 3-8h4"/></svg></div>
      <span className="nd n1">IMU Data</span><span className="nd n2">Federated Learning</span><span className="nd n3">CNN</span><span className="nd n4">BiLSTM</span><span className="nd n5">FiLM</span><span className="nd n6">FastAPI</span><span className="nd n7">Plotly</span><span className="nd n8">PDF Reports</span>
    </div>
  </section>

  <section className="lp-wrap" id="start">
    <div className="lp-final">
      <h2>Ready to analyze your first recording?</h2>
      <p className="sub">Open the portal to upload a session, browse patients or explore population statistics.</p>
      <div className="lp-cta"><Link to="/portal" className="lp-btn pri lg">Get Started <svg className="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M7 17L17 7M8 7h9v9"/></svg></Link><Link to="/subjects" className="lp-btn gho lg">Explore Patients</Link><Link to="/stats" className="lp-btn gho lg">Population Stats</Link></div>
    </div>
  </section>

  <footer className="lp-foot"><div className="lp-wrap">
    <span>© GaitSense. Clinical research tool, not a diagnostic device.</span>
    <nav><Link to="/upload">Upload</Link><Link to="/subjects">Patients</Link><Link to="/stats">Statistics</Link></nav>
  </div></footer>
</div>

  );
}
