// --- Authentication Logic ---

// 1. Login Function
async function login(email, password) {
    try {
        const res = await fetch(`${API_URL.AUTH}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Login failed");
        }

        // Save session data
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("role", data.role);
        localStorage.setItem("name", data.name);

        // Redirect based on role
        redirectToDashboard(data.role);

    } catch (err) {
        alert("Login Error: " + err.message);
    }
}

// 2. Signup Function
async function signup(userData) {
    try {
        const res = await fetch(`${API_URL.AUTH}/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userData)
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Signup failed");
        }

        alert("Registration Successful! Please wait for approval.");
        window.location.href = "../index.html"; // Go back to login

    } catch (err) {
        alert("Error: " + err.message);
    }
}

// 3. Logout Function
function logout() {
    localStorage.clear();
    window.location.href = "/frontend/index.html"; // Adjust path as needed
}

// 4. Get Token Helper (For API calls)
function getToken() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/frontend/index.html"; // Force login
        return null;
    }
    return token;
}

// 5. Page Protection (Call this at the top of dashboard pages)
function checkAuthRole(requiredRole) {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if (!token) {
        window.location.href = "/frontend/index.html";
        return;
    }

    if (role !== requiredRole) {
        window.location.href = "/frontend/pages/unauthorized.html";
    }
}

// 6. Redirect Helper
function redirectToDashboard(role) {
    const paths = {
        'Developer': 'pages/developer/dashboard.html',
        'Principal': 'pages/principal/dashboard.html',
        'HOD': 'pages/hod/dashboard.html',
        'Student': 'pages/student/dashboard.html'
    };
    
    if (paths[role]) {
        window.location.href = paths[role];
    } else {
        alert("Unknown Role: " + role);
    }
}