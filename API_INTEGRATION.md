# API Integration Guide

## Base URL
```
http://localhost:8080/api
```

## Authentication
Currently no authentication required. For production, implement API key authentication.

## Endpoints

### 1. Locations Management

#### Create Location
```http
POST /api/locations
Content-Type: application/json

{
  "name": "Downtown Office",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "insurer_id": "INS-001",
  "policy_ids": ["POL-12345", "POL-67890"]
}
```

Response:
```json
{
  "id": "loc-uuid-here",
  "name": "Downtown Office",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "insurer_id": "INS-001",
  "policy_ids": ["POL-12345", "POL-67890"],
  "created_at": "2025-12-27T10:00:00Z"
}
```

#### List Locations
```http
GET /api/locations
GET /api/locations?insurer_id=INS-001
```

#### Get Location
```http
GET /api/locations/{location_id}
```

### 2. Parametric Triggers

#### Create Trigger
```http
POST /api/triggers
Content-Type: application/json

{
  "location_id": "loc-uuid-here",
  "trigger_type": "rainfall",
  "threshold_value": 50.0,
  "threshold_operator": "gt",
  "duration_hours": 1,
  "payout_amount": 10000.0,
  "active": true
}
```

**Trigger Types:**
- `rainfall` - Rainfall in mm/hour
- `wind_speed` - Wind speed in m/s
- `temperature` - Temperature in °C
- `flood_risk` - Flood risk index
- `drought` - Drought index

**Operators:**
- `gt` - Greater than
- `gte` - Greater than or equal
- `lt` - Less than
- `lte` - Less than or equal
- `eq` - Equal to

#### List Triggers
```http
GET /api/triggers/location/{location_id}
```

#### Toggle Trigger
```http
PATCH /api/triggers/{trigger_id}/toggle
```

### 3. Alerts

#### Get Active Alerts
```http
GET /api/alerts?active_only=true
GET /api/alerts?risk_level=critical
GET /api/alerts/location/{location_id}
```

Response:
```json
[
  {
    "id": "alert-uuid",
    "location_id": "loc-uuid",
    "trigger_id": "trigger-uuid",
    "risk_level": "high",
    "message": "rainfall threshold exceeded: 55.0 gt 50.0",
    "current_value": 55.0,
    "threshold_value": 50.0,
    "triggered_at": "2025-12-27T10:30:00Z",
    "resolved": false,
    "prescriptive_actions": [
      "Deploy emergency drainage equipment",
      "Alert policyholders in affected area",
      "Prepare claims processing team"
    ]
  }
]
```

#### Resolve Alert
```http
PATCH /api/alerts/{alert_id}/resolve
```

### 4. Weather Forecasts

#### Get Current Weather
```http
GET /api/forecast/{location_id}/current
```

Response:
```json
{
  "location_id": "loc-uuid",
  "timestamp": "2025-12-27T10:00:00Z",
  "temperature": 22.5,
  "rainfall": 5.2,
  "wind_speed": 12.3,
  "humidity": 65.0,
  "pressure": 1013.25
}
```

#### Get 48-Hour Forecast
```http
GET /api/forecast/{location_id}
```

Response:
```json
[
  {
    "location_id": "loc-uuid",
    "forecast_time": "2025-12-27T13:00:00Z",
    "temperature": 23.5,
    "rainfall_probability": 30.0,
    "rainfall_amount": 2.5,
    "wind_speed": 10.5,
    "risk_score": 0.25,
    "potential_triggers": ["trigger-uuid-1"]
  }
]
```

## Webhook Integration

Configure webhook URL in `.env`:
```
ALERT_WEBHOOK_URL=https://your-system.com/webhooks/alerts
```

When an alert is triggered, the platform will POST:
```json
{
  "event": "alert.triggered",
  "alert": {
    "id": "alert-uuid",
    "location_id": "loc-uuid",
    "risk_level": "high",
    "message": "...",
    "prescriptive_actions": [...]
  },
  "timestamp": "2025-12-27T10:30:00Z"
}
```

## Error Responses

```json
{
  "detail": "Location not found"
}
```

Status codes:
- `200` - Success
- `201` - Created
- `404` - Not found
- `422` - Validation error
- `500` - Server error

## Rate Limits

No rate limits currently. For production:
- Implement rate limiting per API key
- Recommended: 100 requests/minute per key

## Example Integration (Python)

```python
import requests

API_BASE = "http://localhost:8080/api"

# Create location
location = requests.post(f"{API_BASE}/locations", json={
    "name": "Office Building",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "insurer_id": "INS-001",
    "policy_ids": ["POL-001"]
}).json()

# Create trigger
trigger = requests.post(f"{API_BASE}/triggers", json={
    "location_id": location["id"],
    "trigger_type": "rainfall",
    "threshold_value": 50.0,
    "threshold_operator": "gt",
    "duration_hours": 1,
    "payout_amount": 10000.0
}).json()

# Monitor alerts
alerts = requests.get(
    f"{API_BASE}/alerts/location/{location['id']}"
).json()

for alert in alerts:
    if not alert["resolved"]:
        print(f"ALERT: {alert['message']}")
        print(f"Actions: {alert['prescriptive_actions']}")
```

## Example Integration (JavaScript)

```javascript
const API_BASE = 'http://localhost:8080/api';

// Create location
const location = await fetch(`${API_BASE}/locations`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Office Building',
    latitude: 40.7128,
    longitude: -74.0060,
    insurer_id: 'INS-001',
    policy_ids: ['POL-001']
  })
}).then(r => r.json());

// Get current weather
const weather = await fetch(
  `${API_BASE}/forecast/${location.id}/current`
).then(r => r.json());

console.log(`Current temp: ${weather.temperature}°C`);
```
