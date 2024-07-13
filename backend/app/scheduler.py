from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from api.endpoints.email import send_email_to_all_users

scheduler = AsyncIOScheduler()

async def schedule_task():
    await send_email_to_all_users()

scheduler.add_job(schedule_task, CronTrigger(hour=5,minute=0), id='email_job', replace_existing=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()
