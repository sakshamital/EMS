import asyncio
from app.db.database import db
from app.core.security import get_password_hash

async def create_developer():
    print("--- 👤 Create System Developer ---")
    
    # 1. Input Details
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    phone = input("Enter Phone: ")
    
    # 2. Check if user exists
    if await db["users"].find_one({"email": email}):
        print(f"❌ Error: User with email '{email}' already exists.")
        return

    # 3. Create User Object
    developer_data = {
        "name": name,
        "email": email,
        "password": get_password_hash(password), # Hashes the password securely
        "phone": phone,
        "role": "Developer",       # Hardcoded role
        "approval_status": "Approved", # Auto-approved
        "college_id": None         # Developers don't belong to a college
    }
    
    # 4. Insert into Database
    await db["users"].insert_one(developer_data)
    
    print(f"\n✅ SUCCESS! Developer '{name}' created.")
    print(f"👉 Login with: {email} / {password}")

if __name__ == "__main__":
    # Windows-specific event loop policy
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_developer())