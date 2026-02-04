from fastapi import APIRouter


router = APIRouter()
try:
    from .authRoutes import router as auth_router
    router.include_router(auth_router, prefix="/auth", tags=["auth"])
except Exception as e:
    print(f"[routes] Failed to load authRoutes: {e}")

try:
    from .profileRoutes import router as profile_router
    router.include_router(profile_router, prefix="/profile", tags=["profile"])
except Exception as e:
    print(f"[routes] Failed to load profileRoutes: {e}")

try:
    from .pollRewardRoutes import router as pollReward_router
    router.include_router(pollReward_router, prefix="/poll-reward", tags=["poll-reward"])
except Exception as e:
    print(f"[routes] Failed to load pollRewardRoutes: {e}")

try:
    from .dashboardRoutes import router as dashboard_router
    router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
except Exception as e:
    print(f"[routes] Failed to load dashboardRoutes: {e}")

try:
    from .guideRoutes import router as guide_router
    router.include_router(guide_router, prefix="/guide", tags=["guide"])
except Exception as e:
    print(f"[routes] Failed to load guideRoutes: {e}")

try:
    from .weatherRoutes import router as weather_router
    router.include_router(weather_router, prefix="/weather", tags=["weather"])
except Exception as e:
    print(f"[routes] Failed to load weatherRoutes: {e}")