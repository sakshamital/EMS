// Configuration Settings
// Ensure this matches your backend terminal output EXACTLY
// const API_BASE_URL = "http://127.0.0.1:8000/api";  <-- OLD (Local)
// Use the reliable local IP address and port 8000
// ✅ LIVE BACKEND URL (Render)
// Note: We add '/api' at the end because your routers are prefixed with /api
const API_BASE_URL = "https://ems-5cj4.onrender.com/api"; 

const API_URL = {
    AUTH: `${API_BASE_URL}/auth`,
    DEVELOPER: `${API_BASE_URL}/developer`,
    PRINCIPAL: `${API_BASE_URL}/principal`,
    ADMIN: `${API_BASE_URL}/admin`,
    STUDENT: `${API_BASE_URL}/student`,
    TEACHER: `${API_BASE_URL}/teacher`
};