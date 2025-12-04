from fastapi import APIRouter, Depends, HTTPException, Header, status
from app.services.package_service import package_service
from app.services.storage_service import storage_service
from app.core.config import settings
from app.schemas.package import PackageQueryResponse
from app.schemas.response import ResponseSuccess

router = APIRouter()


async def verify_api_key(
    x_api_key: str = Header(..., description="API Key for client access")
):
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )
    return x_api_key


@router.get(
    "/query",
    response_model=ResponseSuccess[PackageQueryResponse],
    summary="查询包信息 (客户端)",
)
async def query_package(
    package_id: int = None,
    package_name: str = None,
    api_key: str = Depends(verify_api_key),
):
    """
    客户端通过包 ID 或包名称查询包信息及下载链接
    - **package_id**: 包 ID (与 package_name 二选一)
    - **package_name**: 包名称 (与 package_id 二选一)
    - **X-API-Key**: 客户端 API 密钥 (Header)
    """
    if not package_id and not package_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either package_id or package_name must be provided",
        )

    package = await package_service.query_package(package_id, package_name)

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Package not found"
        )

    if not package.is_distributing:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Package distribution is disabled",
        )

    if package.status == "processed_failed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="包处理失败，暂无可用下载链接",
        )

    # Construct download URL
    final_download_url = package.download_url
    if not final_download_url and package.status == "processed_success":
        final_download_url = f"https://{settings.CDN_DOMAIN}/dist/{package.id}/{settings.FIXED_TAG}.{package.type}"

    # Construct original download URL
    original_download_url = None
    if package.r2_original_path:
        original_download_url = storage_service.get_public_url(package.r2_original_path)

    data = PackageQueryResponse(
        package_id=package.id,
        package_name=package.name,
        package_type=package.type,
        version=package.current_version,
        status=package.status,
        download_url=final_download_url,
        original_download_url=original_download_url,
        file_size=package.file_size,
        sha256=package.sha256,
        original_package_version=package.current_version,
        expire_time="",
    )

    return ResponseSuccess(data=data)
