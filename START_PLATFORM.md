# Quick Start Guide

## Prerequisites Checklist
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] OpenWeatherMap API key obtained

## Step 1: Configure API Key

1. Open `.env` file in the project root
2. Replace `your_weather_api_key` with your actual OpenWeatherMap API key:
   ```
   WEATHER_API_KEY=abc123your_actual_key_here
   ```

## Step 2: Start Backend API

Open a terminal and run:

```powershell
# Install Python dependencies (first time only)
pip install -r requirements.txt

# Start the backend API on port 8080
python -m backend.main
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8080
```

Keep this terminal open!

## Step 3: Start Frontend Dashboard

Open a NEW terminal and run:

```powershell
# Navigate to frontend directory
cd frontend

# Install Node dependencies (first time only)
npm install

# Start the Next.js development server
npm run dev
```

You should see:
```
- Local:        http://localhost:3000
```

## Step 4: Access the Platform

Open your browser and go to:
- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8080/docs

## Quick Test

1. In the dashboard, click "Add Location"
2. Enter:
   - Name: "Test Location"
   - Latitude: 40.7128
   - Longitude: -74.0060
   - Insurer ID: "INS-001"
3. Click "Add Location"
4. Go to "Triggers" tab
5. Create a trigger for rainfall > 50mm/h
6. The system will now monitor this location!

## Troubleshooting

### Backend won't start (port 8080 in use)
Try a different port:
```powershell
uvicorn backend.main:app --host 127.0.0.1 --port 8888 --reload
```
Then update the API URL in `frontend/app/components/*.tsx` files.

### Frontend won't start
```powershell
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### No weather data appearing
- Check your API key is correct in `.env`
- Verify the backend is running
- Check browser console for errors (F12)

## What's Running

- **Backend API**: http://localhost:8080
  - Monitors weather every 5 minutes
  - Evaluates parametric triggers
  - Generates alerts

- **Frontend Dashboard**: http://localhost:3000
  - Real-time alert monitoring
  - Location management
  - Trigger configuration
  - Weather forecasts

## Next Steps

1. Add your actual insured locations
2. Configure parametric triggers based on your policies
3. Set up webhook notifications (optional)
4. Integrate with your claims system via API
