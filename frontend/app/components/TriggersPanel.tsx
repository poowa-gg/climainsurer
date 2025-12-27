'use client';

import { useState, useEffect } from 'react';

interface Location {
  id: string;
  name: string;
}

export default function TriggersPanel({ fullWidth = false }: { fullWidth?: boolean }) {
  const [locations, setLocations] = useState<Location[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    location_id: '',
    trigger_type: 'rainfall',
    threshold_operator: 'gt',
    threshold_value: '',
    payout_amount: '',
  });

  useEffect(() => {
    loadLocations();
  }, []);

  const loadLocations = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/locations');
      const data = await response.json();
      setLocations(data);
    } catch (error) {
      console.error('Error loading locations:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8080/api/triggers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          threshold_value: parseFloat(formData.threshold_value),
          payout_amount: formData.payout_amount ? parseFloat(formData.payout_amount) : null,
          duration_hours: 1,
          active: true,
        }),
      });
      
      if (response.ok) {
        setFormData({
          location_id: '',
          trigger_type: 'rainfall',
          threshold_operator: 'gt',
          threshold_value: '',
          payout_amount: '',
        });
        setShowForm(false);
        alert('Trigger created successfully!');
      }
    } catch (error) {
      console.error('Error creating trigger:', error);
    }
  };

  return (
    <div className={`bg-white rounded-xl shadow-2xl p-6 ${fullWidth ? 'col-span-2' : ''}`}>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Parametric Triggers</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
        >
          {showForm ? 'Cancel' : '+ Create Trigger'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="p-4 bg-gray-50 rounded-lg space-y-3">
          <select
            value={formData.location_id}
            onChange={(e) => setFormData({ ...formData, location_id: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg"
            required
          >
            <option value="">Select Location</option>
            {locations.map((loc) => (
              <option key={loc.id} value={loc.id}>{loc.name}</option>
            ))}
          </select>

          <select
            value={formData.trigger_type}
            onChange={(e) => setFormData({ ...formData, trigger_type: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg"
          >
            <option value="rainfall">Rainfall (mm/h)</option>
            <option value="wind_speed">Wind Speed (m/s)</option>
            <option value="temperature">Temperature (°C)</option>
          </select>

          <div className="grid grid-cols-2 gap-3">
            <select
              value={formData.threshold_operator}
              onChange={(e) => setFormData({ ...formData, threshold_operator: e.target.value })}
              className="px-4 py-2 border rounded-lg"
            >
              <option value="gt">Greater Than</option>
              <option value="gte">Greater or Equal</option>
              <option value="lt">Less Than</option>
              <option value="lte">Less or Equal</option>
            </select>
            <input
              type="number"
              step="0.1"
              placeholder="Threshold Value"
              value={formData.threshold_value}
              onChange={(e) => setFormData({ ...formData, threshold_value: e.target.value })}
              className="px-4 py-2 border rounded-lg"
              required
            />
          </div>

          <input
            type="number"
            step="100"
            placeholder="Payout Amount (optional)"
            value={formData.payout_amount}
            onChange={(e) => setFormData({ ...formData, payout_amount: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg"
          />

          <button
            type="submit"
            className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            Create Trigger
          </button>
        </form>
      )}

      <div className="mt-4 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-gray-700">
          Configure parametric triggers to automatically monitor weather conditions and generate alerts when thresholds are exceeded.
        </p>
      </div>
    </div>
  );
}
