from fastapi import APIRouter
from app.api.v1.endpoints import user, blog, comment, auth
from app.middlewares.auth import AdminAuthMiddleware

api_router = APIRouter()

api_router.include_router(auth.router, prefix="", tags=["Auth"])
api_router.include_router(user.router, prefix="/profile", tags=["Profile"])
api_router.include_router(blog.router, prefix="/blog", tags=["Blogs"])
api_router.include_router(comment.router, prefix="/comment", tags=["Comments"])
