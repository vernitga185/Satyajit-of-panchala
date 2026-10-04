from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from challenges.satyajit.routes import router as satyajit_router
from challenges.the_eleventh_day.routes import router as eleventh_day_router

app = FastAPI(title="CTF Challenges", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(satyajit_router, prefix="/api/satyajit", tags=["Satyajit"])
app.include_router(eleventh_day_router, prefix="/api/eleventh", tags=["Eleventh Day"])
