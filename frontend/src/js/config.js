// Configuration Settings
// Ensure this matches your backend terminal output EXACTLY
const API_BASE_URL = "http://127.0.0.1:8000/api"; 

const API_URL = {
    AUTH: `${API_BASE_URL}/auth`,
    // ... rest of the file

    DEVELOPER: `${API_BASE_URL}/developer`,
    PRINCIPAL: `${API_BASE_URL}/principal`,
    ADMIN: `${API_BASE_URL}/admin`,
    STUDENT: `${API_BASE_URL}/student`
};