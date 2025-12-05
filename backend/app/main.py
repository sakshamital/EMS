from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import Routers
from app.routers import auth, developer, principal, admin, student

# Initialize App
app = FastAPI(
    title="EMS API",
    description="Backend for Multi-College Event Management System",
    version="1.0.0"
)

# --- CORS Configuration ---
# Allow all origins for development testing
# ... inside main.py ...

# --- CORS Configuration (THE FIX) ---
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1:5500",  # <--- CRUCIAL: Allow the Live Server port
    "http://localhost:5500",
    "*"                       # Fallback to allow all others
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ... rest of the file ...
# --- CONNECT ROUTERS ---
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(developer.router, prefix="/api/developer", tags=["Developer"])
app.include_router(principal.router, prefix="/api/principal", tags=["Principal"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(student.router, prefix="/api/student", tags=["Student"])

# --- ROOT ROUTE ---
@app.get("/")
def read_root():
    return {
        "status": "online", 
        "message": "EMS Backend is Running!", 
        "docs_url": "http://127.0.0.1:8000/docs"
    }
# ... existing imports ...
from app.routers import auth, developer, principal, admin, student, teacher # <-- Import teacher

# ... inside app ...
app.include_router(teacher.router, prefix="/api/teacher", tags=["Teacher"]) # <-- Include it
from fastapi import FastAPI

app = FastAPI()
