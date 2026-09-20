import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomeView from './views/HomeView';
import GapAnalysisView from './views/GapAnalysisView';
import IntelligenceView from './views/IntelligenceView';
import CareerPathView from './views/CareerPathView';
import { apiClient } from './api/client';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [backendStatus, setBackendStatus] = useState({ online: false, data: null });

  // Probe backend health periodically
  useEffect(() => {
    async function probe() {
      const data = await apiClient.checkHealth();
      if (data) {
        setBackendStatus({ online: true, data });
      } else {
        setBackendStatus({ online: false, data: null });
      }
    }

    probe();
    const interval = setInterval(probe, 8000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-zinc-950 text-zinc-100 antialiased selection:bg-indigo-500 selection:text-white">
      {/* Sticky Frosted Glass Navigation Bar */}
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        backendStatus={backendStatus} 
      />

      {/* Main Viewport Container: max-w-7xl mx-auto px-6 lg:px-8 */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 lg:px-8 py-8">
        {activeTab === 'home' && (
          <HomeView 
            setActiveTab={setActiveTab} 
            backendStatus={backendStatus} 
          />
        )}

        {activeTab === 'gap-analysis' && (
          <GapAnalysisView 
            backendStatus={backendStatus} 
          />
        )}

        {activeTab === 'intelligence' && (
          <IntelligenceView 
            backendStatus={backendStatus} 
          />
        )}

        {activeTab === 'career-path' && (
          <CareerPathView 
            backendStatus={backendStatus} 
          />
        )}
      </main>

      {/* Clean Platform Footer */}
      <Footer />
    </div>
  );
}
