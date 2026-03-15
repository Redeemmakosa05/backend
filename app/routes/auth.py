from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.models import LoginRequest, TokenResponse
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict) -> str:
    s = get_settings()
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=s.access_token_expire_minutes)
    return jwt.encode(payload, s.secret_key, algorithm=s.algorithm)


def verify_token(token: str = Depends(oauth2_scheme)) -> str:
    s = get_settings()
    try:
        payload = jwt.decode(token, s.secret_key, algorithms=[s.algorithm])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    s = get_settings()
    if body.username != s.admin_username or body.password != s.admin_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = create_access_token({"sub": body.username})
    return TokenResponse(access_token=token)
