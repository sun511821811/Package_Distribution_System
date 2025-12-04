from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class PackageBase(BaseModel):
    name: str = Field(..., description="包名称")
    description: Optional[str] = Field(None, description="包描述")
    type: str = Field(..., description="包类型 (如: apk, ipa)")
    current_version: str = Field(..., description="当前版本号")


class PackageCreate(PackageBase):
    pass


class PackageUpdate(BaseModel):
    description: Optional[str] = Field(None, description="包描述")
    is_distributing: Optional[bool] = Field(None, description="是否开启分发")


class PackageOut(PackageBase):
    id: str = Field(..., description="包ID")
    status: str = Field(..., description="处理状态")

    @field_validator("id", mode="before")
    def convert_id_to_str(cls, v):
        return str(v)

    download_url: Optional[str] = Field(None, description="处理后包下载链接")
    original_download_url: Optional[str] = Field(None, description="原包下载链接")
    file_size: Optional[int] = Field(None, description="文件大小")
    sha256: Optional[str] = Field(None, description="SHA256 哈希")
    is_distributing: bool = Field(..., description="是否开启分发")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class PackageQueryResponse(BaseModel):
    package_id: str = Field(..., description="包ID")
    package_name: str = Field(..., description="包名称")
    package_type: str = Field(..., description="包类型")
    version: str = Field(..., description="版本号")
    status: str = Field(..., description="状态")
    download_url: Optional[str] = Field(None, description="下载链接")
    original_download_url: Optional[str] = Field(None, description="原包下载链接")
    file_size: Optional[int] = Field(None, description="文件大小 (字节)")
    sha256: Optional[str] = Field(None, description="文件 SHA256")
    original_package_version: Optional[str] = Field(None, description="原包版本")
    expire_time: str = Field("", description="过期时间")

    @field_validator("package_id", mode="before")
    def convert_id_to_str(cls, v):
        return str(v)
