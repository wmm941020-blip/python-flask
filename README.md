# Flask CRM Project

This is a complete CRM project generated with Flask backend and PureAdminThin frontend.

## Features

- **Employee Management**: Manage users/employees.
- **Position Management**: Manage positions/posts.
- **Role Management**: Manage roles and permissions.
- **Menu Management**: Manage dynamic menus and bind to roles.
- **Work Log**: Employee work logs with async export functionality.
- **Frontend**: PureAdminThin (Vue3 + Vite + ElementPlus).

## Prerequisites

- Python 3.8+
- Node.js 16+
- MySQL 8+ (for Celery async tasks)

## Backend Setup

1. **Install Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Configure Database**:
   - Create a MySQL database named `crm_flask` (utf8mb4).
   - Update `backend/app/config.py` or set `DATABASE_URL` environment variable:
     ```bash
     # Example
     export DATABASE_URL="mysql+pymysql://root:password@localhost/crm_flask"
     ```

3. **Initialize Database**:
   ```bash
   # In the root directory of the repository (flask/python-flask)
   # Make sure your PYTHONPATH includes backend
   
   # Windows
   $env:PYTHONPATH="backend"; python backend/run.py init_db
   $env:PYTHONPATH="backend"; python backend/run.py seed_db
   
   # Linux/Mac
   PYTHONPATH=backend python backend/run.py init_db
   PYTHONPATH=backend python backend/run.py seed_db
   ```
   - Admin: `admin` / `123456`
   - User: `user` / `123456`

4. **Run Backend Server**:
   ```bash
   # Windows
   $env:PYTHONPATH="backend"; python backend/run.py
   
   # Linux/Mac
   PYTHONPATH=backend python backend/run.py
   ```
   Server runs at `http://localhost:5000`.

5. **Run Celery Worker** (Required for Export):
   This project uses MySQL as the Celery broker, so no Redis is needed.
   ```bash
   # Windows
   $env:PYTHONPATH="backend"; celery -A celery_worker.celery worker --pool=solo --loglevel=info
   
   # Linux/Mac
   PYTHONPATH=backend celery -A celery_worker.celery worker --loglevel=info
   ```

## Frontend Setup

1. **Install Dependencies**:
   ```bash
   cd frontend
   pnpm install
   # or
   npm install
   ```

2. **Run Development Server**:
   ```bash
   pnpm dev
   # or
   npm run dev
   ```
   Frontend runs at `http://localhost:8848`.

## Project Structure

- `backend/`: Flask application.
  - `app/api/`: REST APIs.
  - `app/models/`: Database models.
  - `app/tasks/`: Celery tasks (Export).
- `frontend/`: PureAdminThin Vue application.

## API Endpoints

- Auth: `/api/auth/login`, `/api/auth/info`
- Users: `/api/users`
- Roles: `/api/roles`
- Menus: `/api/menus`
- Positions: `/api/positions`
- Logs: `/api/logs`
