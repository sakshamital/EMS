# 🎓 Multi-College Event Management System (EMS)

A comprehensive, web-based platform for managing events across multiple colleges.
Built with **Python (FastAPI)** for the backend and **Vanilla JavaScript + Tailwind CSS** for the frontend.

---

## 🚀 Features

* **Multi-Tenancy:** Supports multiple colleges with data isolation.
* **Role-Based Access:**
    * **Developer:** Creates Colleges & Approves Principals.
    * **Principal:** Approves HODs & Manages Academic Batches.
    * **HOD (Admin):** Approves Student Events & Sign-ups.
    * **Student:** Proposes Events & Registers for them.
* **Real-time Notifications:** Email and SMS integration ready.
* **Responsive UI:** Works on Mobile and Desktop (PWA ready).

---

## 🛠️ Tech Stack

* **Backend:** Python 3.9+, FastAPI, Motor (MongoDB Driver), Pydantic.
* **Database:** MongoDB.
* **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS (via CDN).
* **Deployment:** Docker & Docker Compose.

---

## 📦 How to Run (The Easy Way - Docker)

If you have Docker installed, you can run the entire system with one command.

1.  **Start the System:**
    ```bash
    docker-compose up --build
    ```

2.  **Access the App:**
    * **Frontend (Login):** [http://localhost:3000](http://localhost:3000)
    * **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
    * **Database:** `mongodb://localhost:27017`

---

## 🔧 How to Run (Manual Method - No Docker)

If you don't use Docker, follow these steps to run it locally on Windows/Mac/Linux.

### Prerequisites
* Python 3.8 or higher installed.
* MongoDB installed and running locally on port 27017.

### 1. Setup Backend
1.  Navigate to the backend folder:
    ```bash
    cd backend
    ```
2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Start the Server:
    ```bash
    python -m app.main
    # OR
    uvicorn app.main:app --reload
    ```
    *Server will run at `http://localhost:8000`*

### 2. Setup Frontend
1.  Navigate to the frontend folder:
    ```bash
    cd ../frontend
    ```
2.  **No installation needed!** Just open `index.html` in your browser.
    * *Recommended:* Use "Live Server" in VS Code for the best experience.

---

## 🔑 Default Credentials

To start using the system, you need the initial **System Developer** account.

1.  **Seed the Database** (If running manually):
    * There is no automatic seed script in the Python version yet. You can sign up as a **Developer** via the API docs or use the Signup page (`/pages/signup.html`) and manually select "Developer".

2.  **First Login:**
    * **Email:** `dev@ems.com` (or whatever you create)
    * **Password:** `password123`

---

## 📂 Project Structure

```text
ems-python/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── main.py         # App Entry Point
│   │   ├── models/         # Database Schemas
│   │   ├── routers/        # API Endpoints (Auth, Admin, etc.)
│   │   └── db/             # MongoDB Connection
│   └── requirements.txt    # Python Dependencies
│
├── frontend/               # Client Application
│   ├── index.html          # Login Page
│   ├── pages/              # Role-Specific Dashboards
│   └── src/
│       ├── js/             # Logic (Auth, API Calls)
│       └── css/            # Custom Styles
│
└── docker-compose.yml      # Container Configuration