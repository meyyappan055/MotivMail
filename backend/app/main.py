from fastapi import FastAPI
from api.endpoints.quotes import router as quotes_router
from api.endpoints.email import router as email_router
from scheduler import lifespan

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(quotes_router)
app.include_router(email_router)
