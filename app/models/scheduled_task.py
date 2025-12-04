from tortoise import fields, models

class ScheduledTask(models.Model):
    id = fields.IntField(pk=True, description="任务ID")
    package = fields.ForeignKeyField(
        "models.Package", related_name="scheduled_tasks", description="关联的包"
    )
    interval_seconds = fields.IntField(description="执行间隔(秒)")
    last_run_at = fields.DatetimeField(null=True, description="上次执行时间")
    next_run_at = fields.DatetimeField(description="下次执行时间")
    is_active = fields.BooleanField(default=True, description="是否启用")
    
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "scheduled_tasks"
        table_description = "定时任务表"
