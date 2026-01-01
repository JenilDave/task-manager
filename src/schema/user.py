from pydantic import BaseModel

class AuthToken(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class CreateUserPayload(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str