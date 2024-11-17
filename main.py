import os
import uvicorn
from config.db import SessionLocal, create_all_tables
from models.availability import Availability
from scheduler import check_and_reset_availabilities
from apscheduler.triggers.cron import CronTrigger



from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config.db import Base, engine

from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from scheduler import check_and_reset_availabilities

from router import routes 

try:
    create_all_tables()
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error al crear tablas: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.start()
    
    def job_wrapper():
        db = SessionLocal()
        print("Running job")
        if db.query(Availability).count() == 0:
            check_and_reset_availabilities(db)
        db.close()

    scheduler.add_job(job_wrapper, trigger=CronTrigger(day_of_week="sun", hour=0, minute=0))
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)