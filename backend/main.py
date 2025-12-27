from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from .routers import locations, alerts, forecasts, triggers
from .services.monitor import ParametricMonitor
from .config import settings

monitor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global monitor
    monitor = ParametricMonitor()
    await monitor.start()
    yield
    await monitor.stop()

app = FastAPI(
    title="Hyperlocal Intelligence Platform",
    description="Location-specific forecasts and parametric triggers for insurers",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(locations.router, prefix="/api/locations", tags=["locations"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(forecasts.router, prefix="/api/forecast", tags=["forecasts"])
app.include_router(triggers.router, prefix="/api/triggers", tags=["triggers"])

@app.get("/")
async def root():
    return {"status": "active", "service": "Hyperlocal Intelligence Platform"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
