from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime

# users schema
class UserCreate(BaseModel):
    name:str = Field(min_length=1,max_length=50)
    email:str =Field(min_length=10,max_length=100)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    name:str =Field(min_length=1,max_length=50)
    email:str = Field(min_length=10,max_length=100)
    created_at:datetime
    
# blog schema
class BlogCreate(BaseModel):
    title:str = Field(min_length=1, max_length=200)
    content:str = Field(min_length=1)
    published:bool = Field(default=False)
    user_id:int 
    
class BlogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    title:str=Field(min_length=1, max_length=200)
    content:str = Field(min_length=1)
    published:bool = Field(default=False)
    user_id:int
    created_at:datetime

class BlogWithAuthorOut(BlogOut):
    author_name:str=Field(min_length=1,max_length=50)

class BlogListOut(BaseModel):
    data:list[BlogOut]
    total:int
    
class UserReportOut(BaseModel):
    name:str
    blog_count:int
    
    
class BlogUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    published: bool = False