from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
 
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AuthorityCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    registration_code: str
    department:str


class ComplaintSubmission(BaseModel):
    content: str
    location: str
    
class StatusUpdate(BaseModel):
    complaint_id: int
    status: str


class DepartmentUpdate(BaseModel):
    complaint_id: int
    department: str
