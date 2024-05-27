from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import engine, Base
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Limiter is a class that allows you to limit the
# number of requests a client can make to an endpoint.

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    print("App starts")
    Base.metadata.create_all(bind=engine)
