from fastapi import APIRouter, HTTPException, status
from app.db.database import db
from app.models.user import UserCreate, UserLogin
from app.core.config import settings
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

# --- Security Configuration ---
# Use argon2 instead of bcrypt to fix the 72-byte error
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# --- 1. Signup Route ---
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    # Check if email exists
    if await db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user.dict()
    user_dict['password'] = get_password_hash(user.password)
    
    # Auto-approve Developer, others Pending
    if user.role == "Developer":
        user_dict['approval_status'] = "Approved"
    else:
        user_dict['approval_status'] = "Pending"
        
    new_user = await db["users"].insert_one(user_dict)
    return {"message": "User created", "id": str(new_user.inserted_id)}

# --- 2. Login Route (THIS WAS MISSING/BROKEN) ---
@router.post("/login")
async def login(user: UserLogin):
    # 1. Find user by email
    db_user = await db["users"].find_one({"email": user.email})
    
    # 2. Verify user exists and password matches
    if not db_user or not verify_password(user.password, db_user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 3. Check Approval Status
    if db_user.get('approval_status') != "Approved":
        raise HTTPException(status_code=403, detail="Account pending approval")
        
    # 4. Generate Token
    token = create_access_token({"sub": db_user['email'], "role": db_user['role']})
    
    return {
        "access_token": token, 
        "token_type": "bearer", 
        "role": db_user['role'], 
        "name": db_user['name'],
        "college_id": str(db_user.get('college_id', ''))
    }