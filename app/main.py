from fastapi import FastAPI
from app.auth import router as auth_router
from app.database import engine
from app import models
from app.middleware import protect_endpoints
from app.quotes import quote_router
# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.middleware("http")(protect_endpoints)

# Include authentication routes
app.include_router(auth_router)
app.include_router(quote_router)