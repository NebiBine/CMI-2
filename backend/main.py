from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
import sentry_sdk
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from .services.weather import getWeather
from .database.servicesDb.databaseServ import getCities

#error catcher sentry
sentry_sdk.init(
    dsn="https://769027d1fb68562f85f2557cd62e04fa@o4510619949268992.ingest.de.sentry.io/4510619961262160",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

#scheduler za vreme
scheduler = AsyncIOScheduler()
async def refreshWeather():
    cities = await getCities()
    await getWeather(cities)
    print("[scheduler] Weather data refreshed")

@asynccontextmanager
async def lifespan(_: FastAPI):
    await refreshWeather()
    print("[lifespan] Initial weather refresh completed")
    scheduler.add_job(refreshWeather, 'interval', hours=3)
    scheduler.start()
    print("[lifespan] Scheduler started")
    yield
    scheduler.shutdown()
    print("[lifespan] Scheduler shut down")



app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


# Debug: list routes
for r in app.routes:
    try:
        print("[route]", r.path, sorted(r.methods))
    except Exception:
        pass

# Run from the project root (D:\cmi\cmiIntegracija):
#  py -3.12 -m uvicorn backend.main:app --reload
#  py -3.12 -m pip install -r requirements.txt
#Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process za front

#za db:
#instaliri iz googla: https://www.mongodb.com/try/download/community
#Start-Service -Name MongoDB



# ce so naslednic tezave:
#py -3.12 -m uvicorn backend.main:app --reload --log-level debug --host 0.0.0.0 --port 8000

"""
Always stop other uvicorn/python servers first (taskkill /F /IM python.exe if needed).
Keep this terminal open; you’ll see logs for every request.
Point your frontend to the same host/port (http://localhost:8000 or http://127.0.0.1:8000).
"""



