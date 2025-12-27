import { useState } from 'react'
import AlertsPanel from './components/AlertsPanel'
import LocationsPanel from './components/LocationsPanel'
import TriggersPanel from './components/TriggersPanel'
import ForecastPanel from './components/ForecastPanel'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            Hyperlocal Intelligence Platform
          </h1>
          <p className="text-xl text-blue-200">
            Parametric Insurance Monitoring & Risk Management
          </p>
        </header>

        <nav className="flex justify-center gap-4 mb-8 flex-wrap">
          {['dashboard', 'locations', 'triggers', 'alerts'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                activeTab === tab
                  ? 'bg-white text-purple-900'
                  : 'bg-purple-800 text-white hover:bg-purple-700'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </nav>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {activeTab === 'dashboard' && (
            <>
              <AlertsPanel />
              <ForecastPanel />
              <LocationsPanel />
              <TriggersPanel />
            </>
          )}
          {activeTab === 'locations' && <LocationsPanel fullWidth />}
          {activeTab === 'triggers' && <TriggersPanel fullWidth />}
          {activeTab === 'alerts' && <AlertsPanel fullWidth />}
        </div>
      </div>
    </div>
  )
}

export default App
