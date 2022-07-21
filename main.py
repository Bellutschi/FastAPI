from typing import Optional
from fastapi import Body, FastAPI
import uvicorn
from pydantic import BaseModel # schema validation
from random import randrange

app = FastAPI()

# class for schema validation; inherits from pydantic
# checks the values in body for the data types in class Post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # does the same thing as just default values
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favourite foods", "content": "Pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

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
def get_post(id: int):
    post = find_post(id)
    print(id)
    return {"post_detail": post}

@app.post("/posts")
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
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)