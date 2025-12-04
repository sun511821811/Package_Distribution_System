from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ScheduledTaskBase(BaseModel):
    package_id: str = Field(..., description="包ID")
    interval_seconds: int = Field(..., description="执行间隔(秒)")
    is_active: bool = Field(True, description="是否启用")

    @field_validator("package_id", mode="before")
    def convert_id_to_str(cls, v):
        return str(v)

class ScheduledTaskCreate(ScheduledTaskBase):
    pass

class ScheduledTaskUpdate(BaseModel):
    interval_seconds: Optional[int] = Field(None, description="执行间隔(秒)")
    is_active: Optional[bool] = Field(None, description="是否启用")

class ScheduledTaskOut(ScheduledTaskBase):
    id: int = Field(..., description="任务ID")
    last_run_at: Optional[datetime] = Field(None, description="上次执行时间")
    next_run_at: datetime = Field(..., description="下次执行时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    package_name: Optional[str] = Field(None, description="包名称")

    class Config:
        from_attributes = True
