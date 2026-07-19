from passlib.context import CryptContext
from datetime import datetime, UTC, timedelta
from jose import JWTError,jwt
from app.core.config import settings


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against its hash.
    """
    return pwd_context.verify(
        plain_password, hashed_password
    )

def create_access_token(data:dict,)->str:
    to_encode=data.copy()
    expire=datetime.now(UTC)+timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    to_encode.update(
        {
            "exp":expire,
            "type":"access",
        }
    )
    
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    
def create_refresh_token(data:dict,)->str:
    to_encode=data.copy()
    expire=datetime.now(UTC)+timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    to_encode.update(
        {
            "exp":expire,
            "type":"refresh",
        }
    )
    
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    
def decode_token(token:str,)->dict:
    try:
        payload=jwt.decode(
            token,settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        raise ValueError("Invlaid or Expired token.")