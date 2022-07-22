from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
import uvicorn
from pydantic import BaseModel # schema validation
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# class for schema validation; inherits from pydantic
# checks the values in body for the data types in class Post (trys to cast the specified datatype)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # does the same thing as just default values
    # rating: Optional[int] = None

while True:
    try:
        # RealDictCursor gibt columns und values aus
        conn = psycopg2.connect(host='localhost', database='api', user='postgres', password='kira', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)

# database placeholder
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favourite foods", "content": "Pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

# app.get() als path operation decorator 
# http request get als operation
# "/" als path bzw. route

# root() als path operation function
@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# path parameter id in url wird extrahiert
# VORSICHT!!! path parameter könnte mit einem anderen path matchen (z.B. /posts/latest)
@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # gleiche Vorgehensweise
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    print(id)
    return {"post_detail": post}

# status_code Parameter wird gesetzt
@app.post("/posts", status_code=status.HTTP_201_CREATED)
# Body liest den request body aus
#def create_posts(payload: dict = Body(...)):
    #print(payload)
    #return {"new_post": f"title {payload['title']} content {payload['content']}"}

# parameter gets the pydantic model Post as validation schema
# In Post wird der request body validiert und abgespeichert
def create_posts(new_post: Post):
    print(new_post)
    print(new_post.title)
    print(new_post.published)
    print(new_post.rating)
    print(new_post.dict())
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=30000, reload=True)