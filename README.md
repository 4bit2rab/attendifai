# Employee Attendance Tracker (Desktop Application)

## Overview
This project is a **desktop attendance tracking application** with a FastAPI backend.  
It tracks **productive, idle, and overtime hours** of employees and allows managers to monitor performance, assign shifts, approve overtime, and generate reports.  

**Key Features:**
- Employee registration with **token-based authentication**
- Shift management (create, update, delete, assign)
- Daily productivity tracking (productive, idle, overtime)
- Global activity threshold for idle tracking
- Overtime approval notifications
- Managers can approve or reject overtime hours
- Generate detailed reports and analytics
- Desktop client built with **PyQt6**

---

## Backend Setup (FastAPI)

1. Open a terminal and navigate to the backend folder:  cd backend

2. Create and activate a virtual environment:
- Linux/macOS
    - python -m venv venv
    - source venv/bin/activate
- Windows
    - python -m venv venv
    - venv\Scripts\activate

3. Install dependencies:
    - pip install -r requirements.txt


4. Start the backend server:
    - uvicorn backend.app.api.main:app --reload
    - The server will run at http://127.0.0.1:8000

5. CORS is enabled for http://localhost:5173 to allow the frontend to connect.

6. Desktop Client Setup (PyQt6)
    - Create and activate a virtual environment
    - Install Python dependencies:
        - pip install -r requirements.txt

    - Run the desktop application:
        - python desktop_client/app/monitoring/main.py


First-time users:
Enter your email in the registration window to receive a token from the backend.
After registration, the Attendance Tracker window will start.

Usage
- For Managers:
- View daily and monthly productivity reports
- Approve or reject overtime hours
- Assign and manage employee shifts
- Set global activity thresholds

For Employees:
 - Record productive, idle, and overtime hours daily
 - Receive notifications for overtime approvals
    
Notes

- Ensure the backend server is running before starting the desktop client.
- Requires Python
- Check desktop client console if issues occur