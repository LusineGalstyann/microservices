from fastapi import status, HTTPException, Depends, APIRouter,Query
from common import schemas, models
from sqlalchemy.orm import Session
from common.database import get_db
from passlib.context import CryptContext
from typing import List,Optional
from user_service.routers.password_policy import validate_password_complexity

router = APIRouter(prefix="/users", tags=['Users'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    is_valid, message = validate_password_complexity(user.password)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user.email} already exists"
        )
    hashed_password = hash_password(user.password)
    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas.UserOut])
def get_users(email: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),db: Session = Depends(get_db)):
    query = db.query(models.User)
    if email:
        query = query.filter(models.User.email.ilike(f"%{email}%"))  # case-insensitive partial match

    if user_id:
        query = query.filter(models.User.id == user_id)
    users = query.all()
    return users


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does not exist")
    return user
