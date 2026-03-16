from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, applications
#venv\Scripts\activate
#uvicorn app.main:app --reload
app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(applications.router)

@app.get("/")
def home():
    return {"message": "Job Tracker API"}