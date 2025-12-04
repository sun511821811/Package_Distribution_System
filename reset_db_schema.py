from app.db.session import TORTOISE_ORM
from tortoise import Tortoise, run_async

async def init():
    print("Initializing Tortoise...")
    await Tortoise.init(config=TORTOISE_ORM)
    conn = Tortoise.get_connection("default")
    
    print("Dropping tables...")
    # Disable foreign key checks to avoid errors during drop
    await conn.execute_query("SET FOREIGN_KEY_CHECKS = 0;")
    
    tables_to_drop = ["process_tasks", "original_package_history", "packages"]
    for table in tables_to_drop:
        try:
            await conn.execute_query(f"DROP TABLE IF EXISTS {table};")
            print(f"Dropped {table}")
        except Exception as e:
            print(f"Error dropping {table}: {e}")
            
    await conn.execute_query("SET FOREIGN_KEY_CHECKS = 1;")
    
    print("Recreating schemas...")
    await Tortoise.generate_schemas()
    print("Database reset complete.")

if __name__ == "__main__":
    run_async(init())
