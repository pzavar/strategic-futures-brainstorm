import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Landing } from './pages/Landing';
import { Home } from './pages/Home';
import { Dashboard } from './pages/Dashboard';
import { AnalysisViewPage } from './pages/AnalysisViewPage';
import { TermsOfUse } from './pages/TermsOfUse';

function App() {
  return (
    <Router>
        <div className="min-h-screen bg-gray-50 flex flex-col">
          <Navbar />
          <div className="flex-grow">
            <Routes>
              <Route path="/" element={<Landing />} />
              <Route path="/terms" element={<TermsOfUse />} />
            <Route path="/app" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/analyses/:id" element={<AnalysisViewPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
          <footer className="bg-gray-800 text-gray-300 py-4 mt-auto">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                <p className="text-sm">
                  © {new Date().getFullYear()} Strategic Futures AI. All rights reserved.
                </p>
                <div className="flex gap-6">
                  <Link
                    to="/terms"
                    className="text-sm hover:text-white transition-colors"
                  >
                    Terms of Use
                  </Link>
                </div>
              </div>
            </div>
          </footer>
        </div>
    </Router>
  );
}

export default App;

