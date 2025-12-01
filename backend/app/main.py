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

# --- CORS (Allow Frontend Connection) ---
origins = ["*"] # Allow all for development

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONNECT ROUTERS ---
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(developer.router, prefix="/api/developer", tags=["Developer"])
app.include_router(principal.router, prefix="/api/principal", tags=["Principal"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(student.router, prefix="/api/student", tags=["Student"])

# --- ROOT ROUTE (Fixes the "Not Found" on Homepage) ---
@app.get("/")
def read_root():
    return {
        "status": "online", 
        "message": "EMS Backend is Running!", 
        "docs_url": "http://127.0.0.1:8000/docs"
    }