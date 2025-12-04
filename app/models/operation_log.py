from tortoise import fields, models

class OperationLog(models.Model):
    id = fields.IntField(pk=True, description="日志ID")
    user = fields.ForeignKeyField("models.User", related_name="logs", null=True, description="操作用户")
    username = fields.CharField(max_length=50, null=True, description="用户名 (冗余存储)")
    
    action = fields.CharField(max_length=50, description="操作动作 (如: upload, replace)")
    target_type = fields.CharField(max_length=50, description="操作对象类型 (如: package, user)")
    target_id = fields.CharField(max_length=50, null=True, description="操作对象ID")
    
    details = fields.TextField(null=True, description="操作详情 (JSON)")
    ip_address = fields.CharField(max_length=50, null=True, description="IP 地址")
    
    created_at = fields.DatetimeField(auto_now_add=True, description="操作时间")

    class Meta:
        table = "operation_logs"
        table_description = "系统操作日志表"
