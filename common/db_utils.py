# common/db_utils.py
from sqlalchemy.orm import Session
from common import models, schemas
from fastapi import HTTPException, status


def handle_post_operation(method: str, db: Session, payload=None, post_id=None):
    match method:
        case "get_all":
            return db.query(models.Post).all()

        case "get_by_id":
            post = db.query(models.Post).filter(models.Post.id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            return post

        case "create":
            try:
                new_post = models.Post(**payload.dict())
                db.add(new_post)
                db.commit()
                db.refresh(new_post)
                return new_post
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Create failed: {str(e)}")

        case "update":
            post_query = db.query(models.Post).filter(models.Post.id == post_id)
            post = post_query.first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            post_query.update(payload.dict())
            db.commit()
            return post_query.first()

        case "delete":
            post_query = db.query(models.Post).filter(models.Post.id == post_id)
            post = post_query.first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            post_query.delete()
            db.commit()
            return {"detail": "Post deleted"}

        case _:
            raise HTTPException(status_code=400, detail="Unsupported operation")
