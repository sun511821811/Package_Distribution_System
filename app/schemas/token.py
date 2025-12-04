from pydantic import BaseModel, Field
from typing import Optional


class Token(BaseModel):
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(..., description="令牌类型 (Bearer)")


class TokenData(BaseModel):
    username: Optional[str] = Field(None, description="用户名")
