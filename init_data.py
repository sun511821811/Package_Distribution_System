import asyncio
from app.models.user import User
from app.core.security import get_password_hash
from app.db.session import TORTOISE_ORM
from tortoise import Tortoise

async def init():
    print("Initializing data...")
    await Tortoise.init(config=TORTOISE_ORM)
    
    # Create admin user
    admin_user = await User.get_or_none(username="admin")
    if not admin_user:
        print("Creating admin user...")
        await User.create(
            username="admin",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        print("Admin user created.")
    else:
        print("Admin user exists. Resetting password...")
        admin_user.password_hash = get_password_hash("admin123")
        await admin_user.save()
        print("Admin password reset.")

    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init())
