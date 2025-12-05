from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. IMPORT THE ROUTERS
from app.routers import auth, developer, principal, admin, student

app = FastAPI(
    title="EMS API",
    description="Backend for Multi-College Event Management System",
    version="1.0.0"
)

# ... existing imports ...

app = FastAPI(
    title="EMS API",
    # ...
)

# --- CORS Configuration ---
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://ems-seven-ruby.vercel.app",  # <--- ADD YOUR VERCEL DOMAIN HERE
    "https://ems-1oigkwkq7-sakshams-projects-122dde0a.vercel.app", # <--- ADD THIS ONE TOO (from your screenshot)
    "*"  # Keep this as a fallback for now
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Use the list we just made
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... rest of file ...

# 2. INCLUDE THE ROUTERS (This is what was missing!)
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(developer.router, prefix="/api/developer", tags=["Developer"])
app.include_router(principal.router, prefix="/api/principal", tags=["Principal"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(student.router, prefix="/api/student", tags=["Student"])

@app.get("/")
def read_root():
    return {"message": "EMS Python Backend is Running Successfully!"}