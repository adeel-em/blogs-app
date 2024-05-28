from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import engine, Base
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter
from app.core.redis import on_shutdown

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

app.add_event_handler("shutdown", on_shutdown)


@app.on_event("startup")
async def startup_event():
    print("App starts")
    Base.metadata.create_all(bind=engine)
