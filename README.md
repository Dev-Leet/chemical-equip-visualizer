# Chemical Equipment Parameter Visualizer

A full-stack application designed to analyze, visualize, and report on chemical equipment parameters (Flowrate, Pressure, Temperature). This project consists of three main components:

1. **Backend:** A Django REST Framework API for data processing and storage.
2. **Web Frontend:** A React.js dashboard for browser-based access.
3. **Desktop Frontend:** A PyQt5 application for native desktop usage.

---

## 🚀 Features

* **Data Ingestion:** Secure CSV upload with automated validation and parsing.
* **Statistical Analysis:** Automatic calculation of averages, min/max values, and equipment type distributions.
* **Visualization:** Interactive Doughnut and Bar charts for equipment parameters.
* **Reporting:** On-demand generation of detailed PDF reports.
* **Cross-Platform:** Access data via a modern Web UI or a dedicated Desktop Client.
* **Authentication:** Token-based authentication system (Register/Login).

---

## 🛠️ Tech Stack

### Backend

* **Framework:** Django 4.2.7 & Django REST Framework 3.14.0
* **Data Processing:** Pandas 2.1.0
* **Reporting:** ReportLab 4.0.7
* **Database:** SQLite3 (Default) / Postgres-ready

### Web Frontend

* **Core:** React 18, Vite 5
* **State/Routing:** React Router DOM 6.20
* **Visualization:** Chart.js 4.4, React-Chartjs-2
* **HTTP Client:** Axios

### Desktop Frontend

* **GUI:** PyQt5 5.15.10
* **Plotting:** Matplotlib 3.8.2
* **Data Handling:** Pandas 2.1.4

---

## 📂 Project Structure

```bash
chemical-equipment-visualizer/
├── backend/                # Django REST API
├── frontend-web/           # React + Vite Application
├── frontend-desktop/       # PyQt5 Desktop Application
├── deployment/             # Docker and Shell scripts
└── README.md
```

---

## ⚡ Installation & Setup

### Option A: Automated Setup (Linux/Mac)

Use the provided setup script to create virtual environments and install dependencies for all services.

```bash
chmod +x deployment/scripts/setup.sh
./deployment/scripts/setup.sh
```

### Option B: Manual Setup

#### 1. Backend Setup

The backend must be running for the frontend applications to work.

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and create admin
python manage.py migrate
python manage.py createsuperuser

# Start the server (Runs on port 8000)
python manage.py runserver
```

#### 2. Web Frontend Setup

```bash
cd frontend-web

# Install Node modules
npm install

# Create environment file
echo "VITE_API_BASE_URL=http://localhost:8000/api" > .env

# Start Development Server (Runs on port 3000)
npm run dev
```

#### 3. Desktop Frontend Setup

```bash
cd frontend-desktop

# Install dependencies (Recommend using a separate venv)
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 🐳 Docker Deployment

To deploy the entire stack (Backend + Nginx serving Frontend) using Docker:

```bash
cd deployment/docker

# Build and start services
docker-compose up -d --build
```

* Backend API: [http://localhost:8000](http://localhost:8000)
* Web Dashboard: [http://localhost:80](http://localhost:80) (Served via Nginx)

---

## 📝 Configuration

### Backend Environment Variables (`backend/.env`)

Create a `.env` file in the `backend/` folder:

```ini
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Desktop Config (`frontend-desktop/config.ini`)

The desktop app generates a `config.ini` on first run. You can modify it to change the target API URL or window size.

---

## 🔍 API Endpoints

| Method | Endpoint                | Description                          |
| ------ | ----------------------- | ------------------------------------ |
| POST   | `/api/auth/login/`      | User login & token retrieval         |
| POST   | `/api/auth/register/`   | User registration                    |
| POST   | `/api/upload/`          | Upload CSV dataset                   |
| GET    | `/api/datasets/list/`   | List all user datasets               |
| GET    | `/api/summary/{id}/`    | Get statistical summary of a dataset |
| GET    | `/api/report/{id}/pdf/` | Download analysis report as PDF      |
