from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=50, unique=True, description="用户名")
    password_hash = fields.CharField(max_length=128, description="密码哈希")
    role = fields.CharField(
        max_length=20,
        default="operator",
        description="角色 (admin: 管理员, operator: 操作员)",
    )
    is_active = fields.BooleanField(default=True, description="是否激活")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "users"
        table_description = "系统用户表"
