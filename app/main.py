from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, applications
from fastapi.middleware.cors import CORSMiddleware
#venv\Scripts\activate
#uvicorn app.main:app --reload
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(applications.router)

@app.get("/")
def home():
    return {"message": "Job Tracker API"}