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

1. Open a terminal

2. Create and activate a virtual environment:
- Linux/macOS
    - python -m venv venv
    - source venv/bin/activate
- Windows
    - python -m venv venv
    - venv\Scripts\activate

3. Install dependencies:
    - pip install -r requirements.txt 

4. Import the MySQL Database 
    - An exported MySQL Workbench database file 'test_db.sql' is included to help you get started quickly with preloaded test data.
    - Open MySQL Workbench and import the database.

5. Open backend/app/db/mySqlConfig.py and provide the username and password of MySql Workbench

6. Navigate to the backend folder:  cd backend

7. Start the backend server:
    - uvicorn app.api.main:app --reload
    - The server will run at http://127.0.0.1:8000

8. CORS is enabled for http://localhost:5173 to allow the frontend to connect.

## Desktop Client Setup (PyQt6)

1. Open a new terminal (while Keeping the backend running in other terminal)

2. Activate the same virtual environment if not activated.

3. Run the desktop application:
    - python desktop_client/app/monitoring/main.py

4. With the provided database setup, use `john@gmail.com` to register.

## First-time users:
Enter your email in the registration window to receive a token from the backend.
After registration, the Attendance Tracker window will start.

Note: With the provided database setup, use `john@gmail.com` to register.

## Frontend Setup
1. Open a new terminal (while Keeping the others running in other terminal)

2. Activate the same virtual environment if not activated.

3. Navigate to the backend folder:  cd frontend/manager-dashboard

4. Install depencies:
    - npm install

5. Run 'npm run dev'
    - The frontend will run at: http://localhost:5173

6. Use the following credentials to log in:
    Email: ann@gmail.com
    Password: 1234

> Note: As per the current test database, attendance data is available for January 1 and January 2.

## Usage For Managers:
- View daily and monthly productivity reports
- Approve or reject overtime hours
- Assign and manage employee shifts
- Set global activity thresholds

## Usage For Employees:
 - Record productive, idle, and overtime hours daily
 - Receive notifications for overtime approvals
    
## Notes

- Ensure the backend server is running before starting the desktop client.
- Requires Python
- Check desktop client console if issues occur