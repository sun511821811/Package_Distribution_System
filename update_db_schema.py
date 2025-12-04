from app.db.session import TORTOISE_ORM
from tortoise import Tortoise, run_async

async def init():
    print("Initializing Tortoise...")
    await Tortoise.init(config=TORTOISE_ORM)
    
    print("Generating schemas...")
    # safe=True does not drop tables, only creates missing ones
    await Tortoise.generate_schemas(safe=True)
    print("Schema update complete.")

if __name__ == "__main__":
    run_async(init())
