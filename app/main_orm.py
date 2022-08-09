from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import uvicorn
from pydantic import BaseModel # schema validation
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models, schemas
from database import engine, get_db
from sqlalchemy.orm import Session

# creates all tables stored in Base.metadata
# if __table_name__ is available it doesnt create table
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():

    return {"message": "Hello world!"}



@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts



@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    print(id)
    return post



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    #new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    new_post = models.Post(**new_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
    


if __name__ == "__main__":
    uvicorn.run("main_orm:app", host="localhost", port=30000, reload=True)