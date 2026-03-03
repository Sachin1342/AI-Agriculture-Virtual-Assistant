import React, { useState } from 'react';
import { predictionsAPI } from '../api/client';

const PredictionDashboard = () => {
  const [activeTab, setActiveTab] = useState('groundwater');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  // Groundwater Form
  const [groundwaterForm, setGroundwaterForm] = useState({
    rainfall: 100,
    soil_type: 'loamy',
    temperature: 25,
    humidity: 60,
    previous_level: 5.0,
  });

  // Production Form
  const [productionForm, setProductionForm] = useState({
    crop_type: 'rice',
    area: 1.0,
    rainfall: 100,
    temperature: 25,
    humidity: 60,
    soil_nutrients: 50,
  });

  // Irrigation Form
  const [irrigationForm, setIrrigationForm] = useState({
    crop_type: 'rice',
    area: 1.0,
    season: 'monsoon',
    rainfall: 100,
    soil_type: 'loamy',
  });

  const handleGroundwaterSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await predictionsAPI.groundwaterPrediction(groundwaterForm);
      setResult(response.data);
    } catch (error) {
      setError('Error predicting groundwater: ' + error.message);
    }
    setLoading(false);
  };

  const handleProductionSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await predictionsAPI.productionForecast(productionForm);
      setResult(response.data);
    } catch (error) {
      setError('Error predicting production: ' + error.message);
    }
    setLoading(false);
  };

  const handleIrrigationSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await predictionsAPI.irrigationSchedule(irrigationForm);
      setResult(response.data);
    } catch (error) {
      setError('Error generating schedule: ' + error.message);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-green-50">
      {/* Header */}
      <div className="bg-blue-600 text-white p-8 shadow-lg">
        <h1 className="text-4xl font-bold mb-2">📊 Predictions & Analysis</h1>
        <p className="text-blue-100">Advanced agricultural forecasting tools</p>
      </div>

      {/* Tab Navigation */}
      <div className="flex overflow-x-auto bg-white border-b border-gray-200 sticky top-0 z-10">
        {[
          { id: 'groundwater', label: '💧 Groundwater' },
          { id: 'production', label: '🌾 Crop Yield' },
          { id: 'irrigation', label: '🚿 Irrigation' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => {
              setActiveTab(tab.id);
              setResult(null);
            }}
            className={`px-6 py-4 font-medium transition ${
              activeTab === tab.id
                ? 'text-blue-600 border-b-4 border-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="max-w-7xl mx-auto p-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              {activeTab === 'groundwater' && '💧 Groundwater Prediction'}
              {activeTab === 'production' && '🌾 Crop Production Forecast'}
              {activeTab === 'irrigation' && '🚿 Irrigation Schedule'}
            </h2>


            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                {error}
              </div>
            )}
            <form onSubmit={
              activeTab === 'groundwater' ? handleGroundwaterSubmit :
              activeTab === 'production' ? handleProductionSubmit :
              handleIrrigationSubmit
            }>
              {/* Groundwater Form */}
              {activeTab === 'groundwater' && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Rainfall (mm)
                    </label>
                    <input
                      type="number"
                      value={groundwaterForm.rainfall}
                      onChange={(e) =>
                        setGroundwaterForm({ ...groundwaterForm, rainfall: parseFloat(e.target.value) })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Soil Type
                    </label>
                    <select
                      value={groundwaterForm.soil_type}
                      onChange={(e) =>
                        setGroundwaterForm({ ...groundwaterForm, soil_type: e.target.value })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    >
                      <option>loamy</option>
                      <option>sandy</option>
                      <option>clay</option>
                      <option>silty</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Temperature (°C)
                    </label>
                    <input
                      type="number"
                      value={groundwaterForm.temperature}
                      onChange={(e) =>
                        setGroundwaterForm({ ...groundwaterForm, temperature: parseFloat(e.target.value) })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Humidity (%)
                    </label>
                    <input
                      type="number"
                      value={groundwaterForm.humidity}
                      onChange={(e) =>
                        setGroundwaterForm({ ...groundwaterForm, humidity: parseFloat(e.target.value) })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Previous Water Level (m)
                    </label>
                    <input
                      type="number"
                      value={groundwaterForm.previous_level}
                      onChange={(e) =>
                        setGroundwaterForm({ ...groundwaterForm, previous_level: parseFloat(e.target.value) })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    />
                  </div>
                </div>
              )}

              {/* Production Form */}
              {activeTab === 'production' && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Crop Type
                    </label>
                    <select
                      value={productionForm.crop_type}
                      onChange={(e) =>
                        setProductionForm({ ...productionForm, crop_type: e.target.value })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    >
                      <option>rice</option>
                      <option>wheat</option>
                      <option>corn</option>
                      <option>tomato</option>
                      <option>potato</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Area (hectares)
                    </label>
                    <input
                      type="number"
                      value={productionForm.area}
                      onChange={(e) =>
                        setProductionForm({ ...productionForm, area: parseFloat(e.target.value) })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Rainfall (mm)
                    </label>
                    <input
                      type="number"
                      value={productionForm.rainfall}
                      onChange={(e) =>
                        setProductionForm({ ...productionForm, rainfall: parseFloat(e.target.value) })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Temperature (°C)
                    </label>
                    <input
                      type="number"
                      value={productionForm.temperature}
                      onChange={(e) =>
                        setProductionForm({ ...productionForm, temperature: parseFloat(e.target.value) })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    />
                  </div>
                </div>
              )}

              {/* Irrigation Form */}
              {activeTab === 'irrigation' && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Crop Type
                    </label>
                    <select
                      value={irrigationForm.crop_type}
                      onChange={(e) =>
                        setIrrigationForm({ ...irrigationForm, crop_type: e.target.value })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    >
                      <option>rice</option>
                      <option>wheat</option>
                      <option>corn</option>
                      <option>tomato</option>
                      <option>potato</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Area (hectares)
                    </label>
                    <input
                      type="number"
                      value={irrigationForm.area}
                      onChange={(e) =>
                        setIrrigationForm({ ...irrigationForm, area: parseFloat(e.target.value) })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Season
                    </label>
                    <select
                      value={irrigationForm.season}
                      onChange={(e) =>
                        setIrrigationForm({ ...irrigationForm, season: e.target.value })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    >
                      <option>monsoon</option>
                      <option>summer</option>
                      <option>winter</option>
                      <option>spring</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Soil Type
                    </label>
                    <select
                      value={irrigationForm.soil_type}
                      onChange={(e) =>
                        setIrrigationForm({ ...irrigationForm, soil_type: e.target.value })
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                    >
                      <option>loamy</option>
                      <option>sandy</option>
                      <option>clay</option>
                    </select>
                  </div>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 rounded-lg transition"
              >
                {loading ? 'Processing...' : 'Generate Prediction'}
              </button>
            </form>
          </div>

          {/* Results Section */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">📈 Results</h2>
            
            {!result ? (
              <div className="flex items-center justify-center h-full text-gray-500 text-center">
                <p className="text-lg">Fill the form and click "Generate Prediction" to see results</p>
              </div>
            ) : (
              <div className="space-y-4">
                {result.groundwater_level && (
                  <>
                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                      <p className="text-sm text-gray-600">Groundwater Level</p>
                      <p className="text-2xl font-bold text-blue-600">{result.groundwater_level_meters}</p>
                    </div>
                    <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                      <p className="text-sm text-gray-600">Risk Level</p>
                      <p className="text-2xl font-bold text-yellow-600">{result.risk_level}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-600 mb-2">Recommendations:</p>
                      <ul className="space-y-2">
                        {result.recommendations.map((rec, idx) => (
                          <li key={idx} className="text-sm text-gray-700 flex items-start">
                            <span className="mr-2">✓</span>
                            <span>{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </>
                )}

                {result.total_production_tons && (
                  <>
                    <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                      <p className="text-sm text-gray-600">Expected Yield</p>
                      <p className="text-2xl font-bold text-green-600">{result.total_production_tons} tons</p>
                    </div>
                    <div className="p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                      <p className="text-sm text-gray-600">Quality Score</p>
                      <p className="text-2xl font-bold text-indigo-600">{result.quality_score}</p>
                    </div>
                    {result.market_estimate && (
                      <div className="p-4 bg-orange-50 rounded-lg border border-orange-200">
                        <p className="text-sm text-gray-600">Market Estimate</p>
                        <p className="text-2xl font-bold text-orange-600">₹{result.market_estimate.estimated_total_revenue.toFixed(0)}</p>
                      </div>
                    )}
                  </>
                )}

                {result.schedule && (
                  <div>
                    <p className="text-sm font-medium text-gray-600 mb-2">Schedule:</p>
                    <div className="space-y-2 max-h-48 overflow-y-auto">
                      {result.schedule.slice(0, 6).map((item, idx) => (
                        <div key={idx} className="text-xs text-gray-700 p-2 bg-gray-50 rounded">
                          <p><strong>{item.irrigation_number || item.stage}.</strong> {item.date || item.stage}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionDashboard;
