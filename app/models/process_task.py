from tortoise import fields, models


class ProcessTask(models.Model):
    id = fields.IntField(pk=True, description="任务ID")
    package = fields.ForeignKeyField(
        "models.Package", related_name="tasks", description="关联的包"
    )
    original_package_history = fields.ForeignKeyField(
        "models.OriginalPackageHistory",
        related_name="tasks",
        null=True,
        description="关联的原包历史",
    )

    task_id = fields.CharField(max_length=50, index=True, description="Celery 任务 ID")
    status = fields.CharField(
        max_length=20,
        default="pending",
        description="任务状态 (pending, processing, success, failed)",
    )

    result_message = fields.TextField(null=True, description="处理结果/错误信息")

    retry_count = fields.IntField(default=0, description="重试次数")

    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "process_tasks"
        table_description = "处理任务记录表"
