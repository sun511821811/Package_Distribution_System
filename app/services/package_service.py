from typing import Optional, List
from app.models.package import Package
from app.schemas.package import PackageCreate
from tortoise.expressions import Q


class PackageService:
    async def get_package_by_id(self, package_id: int) -> Optional[Package]:
        return await Package.get_or_none(id=package_id)

    async def get_package_by_name(self, package_name: str) -> Optional[Package]:
        return await Package.get_or_none(name=package_name)

    async def query_package(
        self, package_id: int = None, package_name: str = None
    ) -> Optional[Package]:
        if package_id:
            return await self.get_package_by_id(package_id)
        if package_name:
            return await self.get_package_by_name(package_name)
        return None

    async def create_package(self, data: PackageCreate) -> Package:
        return await Package.create(**data.model_dump())

    async def list_packages(self, skip: int = 0, limit: int = 10) -> List[Package]:
        return await Package.all().offset(skip).limit(limit)


package_service = PackageService()
