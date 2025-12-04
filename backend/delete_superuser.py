import asyncio
from app.db.database import db

async def delete_specific_user():
    print("--- 🗑️  Delete User Tool ---")
    
    # 1. Ask for the Email
    target_email = input("Enter the Email of the user to delete: ")
    
    # 2. Find the user first to confirm they exist
    user = await db["users"].find_one({"email": target_email})
    
    if not user:
        print(f"❌ Error: No user found with email '{target_email}'.")
        return

    # 3. Confirm Deletion
    print(f"\n⚠ Found User: {user['name']} (Role: {user['role']})")
    confirm = input("Are you sure you want to PERMANENTLY delete this user? (yes/no): ")
    
    if confirm.lower() != "yes":
        print("Operation cancelled.")
        return

    # 4. Delete the User
    await db["users"].delete_one({"_id": user["_id"]})
    print(f"✅ SUCCESS! User '{target_email}' has been deleted.")

if __name__ == "__main__":
    # Windows-specific event loop policy
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(delete_specific_user())
    