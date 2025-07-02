from fastapi import FastAPI
from user_service.routers import user
from common.database import init_db

init_db()
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "User Service Running"}
