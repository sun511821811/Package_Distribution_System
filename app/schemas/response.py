from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseBase(BaseModel):
    code: int = Field(
        200,
        description="状态码 (200: 成功, 400: 请求错误, 401: 未授权, 403: 禁止访问, 404: 未找到, 500: 服务器错误)",
    )
    message: str = Field("success", description="状态信息")


class ResponseSuccess(ResponseBase, Generic[T]):
    data: Optional[T] = Field(None, description="响应数据")


class ResponseError(ResponseBase):
    data: Optional[Any] = Field(None, description="错误详情")
