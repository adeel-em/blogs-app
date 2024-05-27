from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import decode_access_token
from app.models.user import User

class AdminAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db):
        self.db = db
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        
        auth_token = request.headers.get("Authorization")
        if not auth_token:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="No authorization header")

        try:
            token = auth_token.split("Bearer ")[1]
            payload = decode_access_token(token)
            if not payload:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

            username = payload.get("sub")
            user = self.db.query(User).filter(User.username == username).first()

            if not user:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
            
            if user.is_active == False:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User deactivated")
            
            if user.role != "admin":
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")
            
            response = await call_next(request)
            return response
        except Exception as e:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")