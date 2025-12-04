import asyncio
from tortoise import Tortoise
from app.core.config import settings
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.user"]},
    )
    # Generate schemas if not exists (for init script usage only, normally Aerich handles this)
    # But here we assume DB might be ready.
    # Actually, for this script to work, we need the table.
    # We can rely on Aerich to have run before this.
    
    username = settings.ADMIN_USERNAME
    password = settings.ADMIN_PASSWORD
    
    if not username or not password:
        print("ADMIN_USERNAME or ADMIN_PASSWORD not set in .env")
        return

    user = await User.filter(username=username).first()
    if user:
        print(f"Admin user {username} already exists.")
    else:
        hashed = pwd_context.hash(password)
        await User.create(username=username, password_hash=hashed, role="admin")
        print(f"Admin user {username} created.")
        
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init())
