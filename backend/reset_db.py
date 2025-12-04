import asyncio
from app.db.database import db
from app.core.security import get_password_hash

async def reset_system():
    print("------------------------------------------------")
    print("⚠  WARNING: PERMANENTLY DELETING ALL DATA...  ⚠")
    print("------------------------------------------------")
    
    # 1. Clear all collections
    users_deleted = await db["users"].delete_many({})
    colleges_deleted = await db["colleges"].delete_many({})
    events_deleted = await db["events"].delete_many({})
    regs_deleted = await db["registrations"].delete_many({})
    
    print(f"🗑️  Deleted {users_deleted.deleted_count} Users")
    print(f"🗑️  Deleted {colleges_deleted.deleted_count} Colleges")
    print(f"🗑️  Deleted {events_deleted.deleted_count} Events")
    print(f"🗑️  Deleted {regs_deleted.deleted_count} Registrations")
    print("✅ Database is now EMPTY.")
    print("------------------------------------------------")

    # 2. Re-seed System Developer
    print("🌱 Re-creating System Developer Account...")
    
    developer_data = {
        "name": "System Developer",
        "email": "dev@ems.com",
        "password": get_password_hash("password123"), # Hashes the password
        "phone": "0000000000",
        "role": "Developer",
        "approval_status": "Approved"
    }
    
    await db["users"].insert_one(developer_data)
    
    print("🎉 SUCCESS! System Reset Complete.")
    print("👉 Login with: dev@ems.com / password123")
    print("------------------------------------------------")

if __name__ == "__main__":
    # Windows-specific event loop policy to prevent errors
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(reset_system())