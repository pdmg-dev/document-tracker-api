# app/schemas/token.py

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(..., min_length=10)
    token_type: str = Field(..., pattern="^bearer$")


class TokenData(BaseModel):
    username: str | None = Field(None, min_length=3)
