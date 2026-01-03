from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI()

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