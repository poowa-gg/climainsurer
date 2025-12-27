'use client';

import { useState, useEffect } from 'react';

interface Location {
  id: string;
  name: string;
}

interface Forecast {
  forecast_time: string;
  temperature: number;
  rainfall_amount: number;
  wind_speed: number;
  risk_score: number;
}

export default function ForecastPanel({ fullWidth = false }: { fullWidth?: boolean }) {
  const [locations, setLocations] = useState<Location[]>([]);
  const [selectedLocation, setSelectedLocation] = useState('');
  const [forecast, setForecast] = useState<Forecast[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadLocations();
  }, []);

  const loadLocations = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/locations');
      const data = await response.json();
      setLocations(data);
      if (data.length > 0) {
        setSelectedLocation(data[0].id);
        loadForecast(data[0].id);
      }
    } catch (error) {
      console.error('Error loading locations:', error);
    }
  };

  const loadForecast = async (locationId: string) => {
    if (!locationId) return;
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8080/api/forecast/${locationId}`);
      const data = await response.json();
      setForecast(data.slice(0, 8)); // Next 24 hours
    } catch (error) {
      console.error('Error loading forecast:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score: number) => {
    if (score >= 0.7) return 'text-red-600';
    if (score >= 0.4) return 'text-orange-600';
    if (score >= 0.2) return 'text-yellow-600';
    return 'text-green-600';
  };

  return (
    <div className={`bg-white rounded-xl shadow-2xl p-6 ${fullWidth ? 'col-span-2' : ''}`}>
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Weather Forecast</h2>
      
      <select
        value={selectedLocation}
        onChange={(e) => {
          setSelectedLocation(e.target.value);
          loadForecast(e.target.value);
        }}
        className="w-full px-4 py-2 border rounded-lg mb-4"
      >
        {locations.map((loc) => (
          <option key={loc.id} value={loc.id}>{loc.name}</option>
        ))}
      </select>

      {loading ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-900 mx-auto"></div>
        </div>
      ) : (
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {forecast.map((item, idx) => (
            <div key={idx} className="p-3 bg-gray-50 rounded-lg flex justify-between items-center">
              <div>
                <p className="text-sm font-semibold">
                  {new Date(item.forecast_time).toLocaleString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </p>
                <p className="text-xs text-gray-600">
                  {item.temperature.toFixed(1)}°C | Rain: {item.rainfall_amount.toFixed(1)}mm | Wind: {item.wind_speed.toFixed(1)}m/s
                </p>
              </div>
              <div className={`font-bold ${getRiskColor(item.risk_score)}`}>
                Risk: {(item.risk_score * 100).toFixed(0)}%
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
