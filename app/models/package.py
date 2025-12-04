from tortoise import fields, models

class Package(models.Model):
    id = fields.BigIntField(pk=True, generated=False, description="包ID (雪花算法)")
    name = fields.CharField(max_length=100, unique=True, index=True, description="包名称")
    description = fields.TextField(null=True, description="包描述")
    type = fields.CharField(max_length=20, description="包类型 (如: apk, ipa, zip)")
    current_version = fields.CharField(max_length=50, description="当前版本号")
    status = fields.CharField(max_length=20, default="pending", description="处理状态 (pending: 等待中, processing: 处理中, processed_success: 处理成功, processed_failed: 处理失败)")
    
    # Processed file info
    download_url = fields.CharField(max_length=500, null=True, description="固定下载链接")
    file_size = fields.BigIntField(null=True, description="文件大小 (字节)")
    sha256 = fields.CharField(max_length=64, null=True, description="文件 SHA256 哈希")
    
    # R2 paths
    r2_original_path = fields.CharField(max_length=500, null=True, description="原包 R2 存储路径")
    r2_processed_path = fields.CharField(max_length=500, null=True, description="处理后包 R2 存储路径")
    
    is_distributing = fields.BooleanField(default=True, description="是否开启分发")
    
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "packages"
        table_description = "分发包信息表"
