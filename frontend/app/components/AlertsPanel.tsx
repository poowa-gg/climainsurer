'use client';

import { useState, useEffect } from 'react';

interface Alert {
  id: string;
  location_id: string;
  risk_level: string;
  message: string;
  current_value: number;
  threshold_value: number;
  triggered_at: string;
  resolved: boolean;
  prescriptive_actions: string[];
}

export default function AlertsPanel({ fullWidth = false }: { fullWidth?: boolean }) {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAlerts();
    const interval = setInterval(loadAlerts, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadAlerts = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/alerts?active_only=true');
      const data = await response.json();
      setAlerts(data);
    } catch (error) {
      console.error('Error loading alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const resolveAlert = async (alertId: string) => {
    try {
      await fetch(`http://localhost:8080/api/alerts/${alertId}/resolve`, {
        method: 'PATCH',
      });
      loadAlerts();
    } catch (error) {
      console.error('Error resolving alert:', error);
    }
  };

  const getRiskColor = (level: string) => {
    const colors = {
      critical: 'bg-red-100 border-red-500 text-red-900',
      high: 'bg-orange-100 border-orange-500 text-orange-900',
      medium: 'bg-yellow-100 border-yellow-500 text-yellow-900',
      low: 'bg-blue-100 border-blue-500 text-blue-900',
    };
    return colors[level as keyof typeof colors] || colors.low;
  };

  return (
    <div className={`bg-white rounded-xl shadow-2xl p-6 ${fullWidth ? 'col-span-2' : ''}`}>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Active Alerts</h2>
      
      {loading ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-900 mx-auto"></div>
        </div>
      ) : alerts.length === 0 ? (
        <p className="text-gray-500 text-center py-8">No active alerts</p>
      ) : (
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`p-4 rounded-lg border-l-4 ${getRiskColor(alert.risk_level)}`}
            >
              <div className="flex justify-between items-start mb-2">
                <div>
                  <span className="font-bold text-sm uppercase">{alert.risk_level}</span>
                  <p className="text-sm mt-1">{alert.message}</p>
                  <p className="text-xs text-gray-600 mt-1">
                    Triggered: {new Date(alert.triggered_at).toLocaleString()}
                  </p>
                </div>
                <button
                  onClick={() => resolveAlert(alert.id)}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm"
                >
                  Resolve
                </button>
              </div>
              
              {alert.prescriptive_actions.length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-300">
                  <p className="font-semibold text-sm mb-2">Recommended Actions:</p>
                  <ul className="list-disc list-inside space-y-1">
                    {alert.prescriptive_actions.map((action, idx) => (
                      <li key={idx} className="text-sm text-gray-700">{action}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
