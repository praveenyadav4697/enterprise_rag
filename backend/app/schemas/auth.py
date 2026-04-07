from pydantic import BaseModel, Field

class AuthRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=200)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
