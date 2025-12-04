from tortoise import fields, models


class OriginalPackageHistory(models.Model):
    id = fields.IntField(pk=True, description="历史记录ID")
    package = fields.ForeignKeyField(
        "models.Package", related_name="history", description="关联的包"
    )
    version = fields.CharField(max_length=50, description="原包内部版本号")

    file_name = fields.CharField(max_length=255, description="文件名")
    file_size = fields.BigIntField(description="文件大小 (字节)")
    sha256 = fields.CharField(max_length=64, description="文件 SHA256 哈希")
    r2_path = fields.CharField(max_length=500, description="R2 存储路径")

    uploaded_by = fields.ForeignKeyField(
        "models.User", related_name="uploaded_packages", null=True, description="上传者"
    )
    created_at = fields.DatetimeField(auto_now_add=True, description="上传时间")

    class Meta:
        table = "original_package_history"
        table_description = "原包上传历史表"
