import { useState, useEffect } from 'react'

const API_BASE = 'http://localhost:8080/api'

export default function LocationsPanel({ fullWidth = false }) {
  const [locations, setLocations] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    latitude: '',
    longitude: '',
    insurer_id: '',
  })

  useEffect(() => {
    loadLocations()
  }, [])

  const loadLocations = async () => {
    try {
      const response = await fetch(`${API_BASE}/locations`)
      const data = await response.json()
      setLocations(data)
    } catch (error) {
      console.error('Error loading locations:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await fetch(`${API_BASE}/locations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          latitude: parseFloat(formData.latitude),
          longitude: parseFloat(formData.longitude),
          policy_ids: [],
        }),
      })
      
      if (response.ok) {
        setFormData({ name: '', latitude: '', longitude: '', insurer_id: '' })
        setShowForm(false)
        loadLocations()
        alert('Location added successfully!')
      }
    } catch (error) {
      console.error('Error adding location:', error)
    }
  }

  return (
    <div className={`bg-white rounded-xl shadow-2xl p-6 ${fullWidth ? 'col-span-2' : ''}`}>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Locations</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
        >
          {showForm ? 'Cancel' : '+ Add Location'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="mb-6 p-4 bg-gray-50 rounded-lg space-y-3">
          <input
            type="text"
            placeholder="Location Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg"
            required
          />
          <div className="grid grid-cols-2 gap-3">
            <input
              type="number"
              step="0.0001"
              placeholder="Latitude"
              value={formData.latitude}
              onChange={(e) => setFormData({ ...formData, latitude: e.target.value })}
              className="px-4 py-2 border rounded-lg"
              required
            />
            <input
              type="number"
              step="0.0001"
              placeholder="Longitude"
              value={formData.longitude}
              onChange={(e) => setFormData({ ...formData, longitude: e.target.value })}
              className="px-4 py-2 border rounded-lg"
              required
            />
          </div>
          <input
            type="text"
            placeholder="Insurer ID"
            value={formData.insurer_id}
            onChange={(e) => setFormData({ ...formData, insurer_id: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg"
            required
          />
          <button
            type="submit"
            className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            Add Location
          </button>
        </form>
      )}

      <div className="space-y-3">
        {locations.map((location) => (
          <div
            key={location.id}
            className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition cursor-pointer"
          >
            <h3 className="font-semibold text-lg">{location.name}</h3>
            <p className="text-sm text-gray-600">
              {location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}
            </p>
            <p className="text-xs text-gray-500 mt-1">Insurer: {location.insurer_id}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
