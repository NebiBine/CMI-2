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