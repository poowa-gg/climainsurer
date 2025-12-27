# Setup Guide

## Prerequisites

- Python 3.11+
- OpenWeatherMap API key (free tier available at https://openweathermap.org/api)
- Docker & Docker Compose (optional, for containerized deployment)

## Step-by-Step Setup

### 1. Get Weather API Key

1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Navigate to API keys section
4. Copy your API key

### 2. Configure Environment

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your API key
# WEATHER_API_KEY=your_actual_api_key_here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Platform

```bash
# Start the API server
python -m backend.main

# The API will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### 5. Open the Dashboard

Open `frontend/index.html` in your web browser to access the monitoring dashboard.

## Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Testing the Platform

### 1. Add a Location

```bash
curl -X POST http://localhost:8000/api/locations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New York Office",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "insurer_id": "INS-001",
    "policy_ids": ["POL-001"]
  }'
```

### 2. Create a Parametric Trigger

```bash
curl -X POST http://localhost:8000/api/triggers \
  -H "Content-Type: application/json" \
  -d '{
    "location_id": "YOUR_LOCATION_ID",
    "trigger_type": "rainfall",
    "threshold_value": 50.0,
    "threshold_operator": "gt",
    "duration_hours": 1,
    "payout_amount": 10000.0
  }'
```

### 3. Check Current Weather

```bash
curl http://localhost:8000/api/forecast/YOUR_LOCATION_ID/current
```

### 4. View Alerts

```bash
curl http://localhost:8000/api/alerts
```

## Troubleshooting

### API Key Issues
- Ensure your OpenWeatherMap API key is active (can take a few hours after signup)
- Check that the key is correctly set in `.env` file
- Verify no extra spaces or quotes around the key

### Connection Errors
- Ensure the API server is running on port 8000
- Check firewall settings
- For Docker: ensure containers are running with `docker-compose ps`

### No Alerts Appearing
- Triggers only fire when thresholds are exceeded
- Check trigger configuration with GET /api/triggers
- Monitor logs for any errors during weather checks

## Production Considerations

1. **Database**: Replace in-memory storage with PostgreSQL
2. **Authentication**: Add API key authentication
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Monitoring**: Set up application monitoring (Prometheus, Grafana)
5. **Webhooks**: Configure alert webhooks for real-time notifications
6. **Scaling**: Use Redis for caching and session management
7. **SSL/TLS**: Enable HTTPS for production deployments
