from fastapi import FastAPI
from user_service.routers import auth
from post_service.routers import post
from common.database import init_db

init_db()
#models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()


app.include_router(post.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
