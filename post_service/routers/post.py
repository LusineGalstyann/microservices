from fastapi import status, Depends, APIRouter, Query
from common import schemas, models
from user_service.routers import oauth2
from sqlalchemy.orm import Session
from common.database import get_db
from typing import List, Optional,Union
from datetime import datetime
from common.db_utils import handle_post_operation
from fastapi.responses import JSONResponse

print("DEBUG - get_db type in post.py:", type(get_db))

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    return handle_post_operation("get_by_id", db=db, post_id=id)


@router.get("/", response_model=List[Union[schemas.Post, schemas.PostPublic]])
def get_posts(
        db: Session = Depends(get_db),
        title: Optional[str] = Query(None, description="Filter by title (substring match)"),
        published: Optional[bool] = Query(None, description="Filter by published status"),
        created_after: Optional[datetime] = Query(None, description="Filter by creation date after"),
        current_user: Optional[schemas.UserOut] = Depends(oauth2.try_get_current_user)
):
    query = db.query(models.Post)

    if title:
        query = query.filter(models.Post.title.ilike(f"%{title}%"))
    if published is not None:
        query = query.filter(models.Post.published == published)
    if created_after:
        query = query.filter(models.Post.created_at > created_after)

    posts = query.all()

    if current_user:
        return [schemas.Post.model_validate(p) for p in posts]
    else:
        return [schemas.PostPublic.model_validate(p) for p in posts]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    return handle_post_operation("create", db=db, payload=post)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    return handle_post_operation("update", db=db, post_id=id, payload=post)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    handle_post_operation("delete", db=db, post_id=id)
    return
