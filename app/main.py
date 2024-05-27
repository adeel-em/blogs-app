from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import engine, Base


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    print("App starts")
    Base.metadata.create_all(bind=engine)
