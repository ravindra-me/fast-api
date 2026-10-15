from pydantic import BaseModel,Field ,ConfigDict

class TaskCreate(BaseModel):
    title:str = Field(min_length=1, max_length=100)
    done:bool = False
    
class TaskOut(BaseModel):
    # from_attributes=True = “dict nahi, object ke attributes se value lo.” Ye line nahi lagayi to error aayega. Ye bahut common interview/debugging point hai.
    model_config = ConfigDict(from_attributes=True)
    id:int
    title:str = Field(min_length=1, max_length=100)
    done:bool =False

class TaskListOut(BaseModel):
    data:list[TaskOut]
    total: int

