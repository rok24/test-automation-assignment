from fastapi import FastAPI
from app.auth import router as auth_router
from app.database import engine
from app import models

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include authentication routes
app.include_router(auth_router)
