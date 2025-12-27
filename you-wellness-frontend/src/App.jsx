import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import GenomicProfile from './pages/GenomicProfile';
import MicrobiomeInsights from './pages/MicrobiomeInsights';
import WearableData from './pages/WearableData';
import BloodTestResults from './pages/BloodTestResults';
import NutritionPlans from './pages/NutritionPlans';
import Appointments from './pages/Appointments';
import Telemedicine from './pages/Telemedicine';
import Sidebar from './components/ui/sidebar';
import { Toaster } from './components/ui/sonner';

function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <main className="flex-1 p-8 lg:p-12">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/genomic-profile" element={<GenomicProfile />} />
            <Route path="/microbiome-insights" element={<MicrobiomeInsights />} />
            <Route path="/wearable-data" element={<WearableData />} />
            <Route path="/blood-test-results" element={<BloodTestResults />} />
            <Route path="/nutrition-plans" element={<NutritionPlans />} />
            <Route path="/appointments" element={<Appointments />} />
            <Route path="/telemedicine" element={<Telemedicine />} />
          </Routes>
        </main>
      </div>
      <Toaster />
    </Router>
  );
}

export default App;
