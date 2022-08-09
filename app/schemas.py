from pydantic import BaseModel


# class for schema validation; inherits from pydantic
# checks the values in body for the data types in class Post (trys to cast the specified datatype)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # does the same thing as just default values
    # rating: Optional[int] = None



class PostCreate(PostBase):
    pass