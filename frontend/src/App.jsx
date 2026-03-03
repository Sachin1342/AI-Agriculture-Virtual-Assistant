import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatbotComponent from './components/ChatbotComponent';
import PredictionDashboard from './components/PredictionDashboard';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/chatbot" element={<ChatbotComponent />} />
        <Route path="/predictions" element={<PredictionDashboard />} />
        <Route path="/" element={<HomePage />} />
      </Routes>
    </Router>
  );
}

const HomePage = () => (
  <div className="min-h-screen bg-gradient-to-br from-green-400 via-blue-500 to-green-600 text-white">
    <div className="flex flex-col items-center justify-center min-h-screen px-4">
      <div className="text-center mb-12">
        <h1 className="text-6xl font-bold mb-4">🌾 Crop Assistant AI</h1>
        <p className="text-xl mb-8 opacity-90">
          Intelligent Agricultural Virtual Assistant
        </p>
        <p className="text-lg opacity-80 mb-12 max-w-2xl mx-auto">
          Powered by AI for disease detection, groundwater analysis, resource management,
          and crop production forecasting
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6 max-w-2xl w-full">
        <a
          href="/chatbot"
          className="bg-white text-green-600 p-8 rounded-lg shadow-lg transform hover:scale-105 transition cursor-pointer"
        >
          <div className="text-4xl mb-4">💬</div>
          <h2 className="text-2xl font-bold mb-2">Chat Assistant</h2>
          <p className="text-sm text-gray-600">
            Ask questions about diseases, crops, water levels, and more
          </p>
        </a>

        <a
          href="/predictions"
          className="bg-white text-blue-600 p-8 rounded-lg shadow-lg transform hover:scale-105 transition cursor-pointer"
        >
          <div className="text-4xl mb-4">📊</div>
          <h2 className="text-2xl font-bold mb-2">Predictions</h2>
          <p className="text-sm text-gray-600">
            Forecast yields, water levels, and irrigation schedules
          </p>
        </a>
      </div>

      <div className="mt-16 grid md:grid-cols-4 gap-4 max-w-4xl w-full text-center">
        <div className="bg-white bg-opacity-20 p-4 rounded-lg backdrop-blur">
          <div className="text-3xl mb-2">🍃</div>
          <p className="font-semibold">Disease Detection</p>
        </div>
        <div className="bg-white bg-opacity-20 p-4 rounded-lg backdrop-blur">
          <div className="text-3xl mb-2">💧</div>
          <p className="font-semibold">Water Analysis</p>
        </div>
        <div className="bg-white bg-opacity-20 p-4 rounded-lg backdrop-blur">
          <div className="text-3xl mb-2">🌾</div>
          <p className="font-semibold">Yield Forecast</p>
        </div>
        <div className="bg-white bg-opacity-20 p-4 rounded-lg backdrop-blur">
          <div className="text-3xl mb-2">⚙️</div>
          <p className="font-semibold">Resource Mgmt</p>
        </div>
      </div>
    </div>
  </div>
);

export default App;
