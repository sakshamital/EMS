import shutil
import os
from fastapi import UploadFile
from uuid import uuid4

# Create a static folder to store images if it doesn't exist
UPLOAD_DIR = "static/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(upload_file: UploadFile) -> str:
    """
    Saves an uploaded file to the disk and returns the file path.
    """
    try:
        # Generate a unique filename to prevent overwriting
        file_extension = upload_file.filename.split(".")[-1]
        unique_filename = f"{uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            
        # Return the relative path (URL accessible)
        return f"/static/images/{unique_filename}"
    
    except Exception as e:
        print(f"Error saving file: {e}")
        return None