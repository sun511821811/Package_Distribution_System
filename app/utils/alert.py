from app.core.config import settings

async def send_dingtalk_alert(message: str):
    if not settings.DINGTALK_WEBHOOK:
        return
    # TODO: Implement DingTalk alert logic
    pass

async def send_email_alert(subject: str, message: str):
    if not settings.EMAIL_SMTP_HOST:
        return
    # TODO: Implement Email alert logic
    pass
