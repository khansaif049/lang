from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class Student(BaseModel):
    name:str ="saif"
    age:Optional[int]=None
    email:EmailStr
    cgpa:float = Field(gt=0,lt=10,default=5,description="A decimal Value represting the cgpa of the student")

new_student = {'name':"rahul",'age':'32',"email":"abc@gmail.com"}

student = Student(**new_student)
dict_student = dict(student)
print(dict_student['name'])