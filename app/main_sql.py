from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
import uvicorn
from pydantic import BaseModel # schema validation
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import schemas

app = FastAPI()


while True:
    try:
        # RealDictCursor gibt columns und values aus
        # psycopg2 Database Driver for postgres
        conn = psycopg2.connect(host='localhost', database='api', user='postgres', password='kira', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)



# app.get() als path operation decorator 
# http request get als operation
# "/" als path bzw. route

# root() als path operation function
@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()

    #return {"data": posts}
    #automatically serealize the data
    return posts

# path parameter id in url wird extrahiert
# VORSICHT!!! path parameter könnte mit einem anderen path matchen (z.B. /posts/latest)
@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # gleiche Vorgehensweise
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    print(id)
    return post

# status_code Parameter wird gesetzt
@app.post("/posts", status_code=status.HTTP_201_CREATED)
# Body liest den request body aus
#def create_posts(payload: dict = Body(...)):
    #print(payload)
    #return {"new_post": f"title {payload['title']} content {payload['content']}"}

# parameter gets the pydantic model Post as validation schema
# In Post wird der request body validiert und abgespeichert
def create_posts(new_post: schemas.PostCreate):

    # nicht mit f-String arbeiten, weil für SQL-Injection anfaellig
    cursor.execute(f""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    new_post = cursor.fetchone()
    conn.commit()
    
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate):
    
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return updated_post
    


if __name__ == "__main__":
    uvicorn.run("main_sql:app", host="localhost", port=30000, reload=True)