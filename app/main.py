from fastapi import FastAPI
from app.config.main import settings
from contextlib import asynccontextmanager
from app.api.routers import all_routers
from fastapi.middleware.cors import CORSMiddleware

openapi_url = None
redoc_url = None

if settings.VISIBILITY_DOCUMENTATION is True:
    openapi_url = "/openapi.json"
    redoc_url = "/redoc"
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    
    
app = FastAPI(lifespan=lifespan, openapi_url=openapi_url, redoc_url=redoc_url)

for router in all_routers:
    app.include_router(router)
    
origins = [settings.WEB_APP_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)