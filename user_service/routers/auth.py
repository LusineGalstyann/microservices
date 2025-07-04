from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from common import models, database
from user_service.routers import oauth2
from user_service.routers.user import verify
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user or not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {'access_token': access_token, "token_type": "bearer"}
