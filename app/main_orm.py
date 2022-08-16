from fastapi import FastAPI
import uvicorn
import models
from database import engine
from routers import post, user, auth, vote
from config import settings

# creates all tables stored in Base.metadata
# if __table_name__ is available it doesnt create table
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# stellt Verbindung zu den einzelnen routers her
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():

    return {"message": "Hello world!"}


if __name__ == "__main__":
    uvicorn.run("main_orm:app", host=settings.database_hostname, port=settings.database_port, reload=True)