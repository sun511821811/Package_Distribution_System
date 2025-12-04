from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., description="用户名")


class UserCreate(UserBase):
    password: str = Field(..., description="密码")
    role: str = Field("operator", description="角色 (admin: 管理员, operator: 操作员)")


class UserOut(UserBase):
    id: int = Field(..., description="用户ID")
    role: str = Field(..., description="角色")
    is_active: bool = Field(..., description="是否激活")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
