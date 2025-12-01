import os

# Define the root project name
PROJECT_NAME = "ems-python"

# Define the folder structure and files
# Key is the path (folders), Value is a list of filenames to create inside
structure = {
    "": ["docker-compose.yml", "README.md"],
    
    "backend": [".env", ".gitignore", "requirements.txt"],
    "backend/app": ["__init__.py", "main.py"],
    "backend/app/core": ["__init__.py", "config.py", "security.py"],
    "backend/app/db": ["__init__.py", "database.py"],
    "backend/app/models": ["__init__.py", "user.py", "college.py", "event.py"],
    "backend/app/routers": ["__init__.py", "auth.py", "developer.py", "principal.py", "admin.py", "student.py"],
    "backend/app/utils": ["__init__.py", "file_upload.py", "notifications.py"],
    
    "frontend": ["index.html"],
    "frontend/pages": ["signup.html", "unauthorized.html"],
    "frontend/pages/developer": ["dashboard.html"],
    "frontend/pages/principal": ["dashboard.html"],
    "frontend/pages/hod": ["dashboard.html"],
    "frontend/pages/student": ["dashboard.html", "create-event.html"],
    
    "frontend/src/css": ["style.css"],
    "frontend/src/js": ["config.js", "auth.js", "utils.js"],
    "frontend/src/js/controllers": ["devController.js", "principalController.js", "hodController.js", "studentController.js"],
    "frontend/src/assets/logos": [],   # Empty folder
    "frontend/src/assets/images": []   # Empty folder
}

# Define content for specific files to get you started
file_contents = {
    "docker-compose.yml": """version: '3.8'
services:
  mongodb:
    image: mongo:latest
    container_name: ems-mongo
    ports:
      - "27017:27017"
    volumes:
      - ./mongo_data:/data/db
""",
    "backend/requirements.txt": """fastapi
uvicorn
motor
python-dotenv
python-multipart
passlib[bcrypt]
pyjwt
email-validator
""",
    "backend/.env": """MONGO_URI=mongodb://localhost:27017/ems_db
SECRET_KEY=change_this_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
""",
    "backend/app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "EMS Backend is running!"}
""",
    "frontend/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>EMS Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="src/js/config.js" defer></script>
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
    <div class="bg-white p-8 rounded shadow-md">
        <h1 class="text-2xl font-bold mb-4">EMS System Login</h1>
        <p>Welcome! Please log in.</p>
    </div>
</body>
</html>
"""
}

def create_structure():
    base_path = os.path.join(os.getcwd(), PROJECT_NAME)
    
    # Create the base project folder
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        print(f"Created root folder: {base_path}")
    else:
        print(f"Folder '{PROJECT_NAME}' already exists. Updating contents...")

    # Iterate over the structure dictionary
    for folder, files in structure.items():
        # Create directory path
        dir_path = os.path.join(base_path, folder)
        os.makedirs(dir_path, exist_ok=True)
        
        # Create files inside the directory
        for filename in files:
            file_path = os.path.join(dir_path, filename)
            
            # Check if we have specific content for this file, otherwise make it empty
            content = file_contents.get(os.path.join(folder, filename).replace("\\", "/"), "")
            
            # Write the file
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  + Created: {os.path.join(folder, filename)}")
            else:
                print(f"  - Skipped (exists): {os.path.join(folder, filename)}")

    print(f"\nSUCCESS! Project '{PROJECT_NAME}' created successfully.")
    print(f"Location: {base_path}")

if __name__ == "__main__":
    create_structure()
    