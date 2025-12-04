import os
from dotenv import load_dotenv

# Force load .env
load_dotenv(override=True)

from app.db.session import TORTOISE_ORM
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings
from tortoise import Tortoise, run_async

async def reset_admin():
    print("Initializing Tortoise...")
    await Tortoise.init(config=TORTOISE_ORM)
    
    username = "admin"
    password = "password"
    
    print(f"Resetting password for {username}...")
    
    user = await User.get_or_none(username=username)
    if user:
        user.password_hash = get_password_hash(password)
        user.role = "admin"
        await user.save()
        print(f"Updated existing user {username}")
    else:
        await User.create(
            username=username,
            password_hash=get_password_hash(password),
            role="admin"
        )
        print(f"Created new user {username}")
        
    print(f"Admin reset complete. Login with {username} / {password}")

if __name__ == "__main__":
    run_async(reset_admin())
