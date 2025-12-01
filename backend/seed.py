import asyncio
from app.db.database import db
from app.core.security import get_password_hash

async def seed_developer():
    print("Checking for Developer account...")
    
    # Check if user exists
    existing_user = await db.users.find_one({"email": "dev@ems.com"})
    
    if existing_user:
        print(f"✅ User already exists!")
        print(f"Email: {existing_user['email']}")
        print("You can log in now.")
    else:
        # Create the user
        developer_data = {
            "name": "System Developer",
            "email": "dev@ems.com",
            "password": get_password_hash("password123"), # Hashes the password
            "role": "Developer",
            "status": "Approved"
        }
        
        await db.users.insert_one(developer_data)
        print("🎉 Developer Account Created Successfully!")
        print("Email: dev@ems.com")
        print("Password: password123")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(seed_developer())