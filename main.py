from typing import Optional
from fastapi import Body, FastAPI
import uvicorn
from pydantic import BaseModel # schema validation

app = FastAPI()

# class for schema validation; inherits from pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # does the same thing as just default values
    rating: Optional[int] = None

# app.get() als path operation decorator 
# http request get als operation
# "/" als path bzw. route

# root() als path operation function
@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.get("/posts")
def get_posts():
    return {"data": "This is my new post."}

@app.post("/createposts")
#def create_posts(payload: dict = Body(...)):
    #print(payload)
    #return {"new_post": f"title {payload['title']} content {payload['content']}"}

#parameter gets the pydantic model Post as validation schema
def create_posts(new_post: Post):
    print(new_post)
    print(new_post.title)
    print(new_post.published)
    print(new_post.rating)
    print(new_post.dict())
    return {"data": new_post}
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)