import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { Layout } from './components/Layout';
import { Home } from './pages/Home';
import { CropPrediction } from './pages/CropPrediction';
import { FertilizerRecommendation } from './pages/FertilizerRecommendation';
import { YieldEstimation } from './pages/YieldEstimation';
import { Dashboard } from './pages/Dashboard';
import { About } from './pages/About';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/crop" element={<CropPrediction />} />
            <Route path="/fertilizer" element={<FertilizerRecommendation />} />
            <Route path="/yield" element={<YieldEstimation />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
