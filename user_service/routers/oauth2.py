from jose import JWTError, jwt
from datetime import datetime, timedelta
from common import schemas, models, database
from fastapi import Depends, status, HTTPException, Request
from fastapi.security import OAuth2, OAuth2PasswordBearer
from typing import Optional
from sqlalchemy.orm import Session

# class OAuth2PasswordBearerOptional(OAuth2PasswordBearer):
#     async def __call__(self, request: Request) -> Optional[str]:
#         authorization: str = request.headers.get("Authorization")
#         scheme, _, param = authorization.partition(" ") if authorization else ("", "", "")
#         if scheme.lower() != "bearer":
#             return None
#         return param
#
# oauth2_scheme_optional = OAuth2PasswordBearerOptional(tokenUrl='login',auto_error=False)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login', auto_error=False)

SECRET_KEY = "a6629af36ee72b510c7fc5a506690854112c0c56feafe64c20c4e436640ffc62"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)


def try_get_current_user(
        token: Optional[str] = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)
) -> Optional[schemas.UserOut]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        user = db.query(models.User).filter(models.User.id == user_id).first()
        return schemas.UserOut.model_validate(user) if user else None
    except JWTError:
        return None
