# 📦 Smart Inventory Management

Smart Inventory is a **FastAPI + Vision AI** project that enables mobile and web users to snap pictures, detect objects, and manage inventory counts automatically.  
This project is designed for the **LiquidAI Hackathon 02**, focusing on privacy-friendly, on-device vision models.

---

## ✨ Features
- 📸 **Camera Capture** — Upload images from mobile or web camera.
- 🤖 **Object Detection** — AI-powered detection and counting of items.
- 📊 **Inventory Logs** — Save detections with summaries for quick insights.
- 🌐 **Web UI** — Lightweight frontend served via Jinja2 templates.
- 🐳 **Dockerized Setup** — Ready for containerized deployment.
- ⚡ **CI/CD** — GitHub Actions workflow for continuous integration.

---

## 📂 Project Structure

```bash
smart_inventory/
│── app/
│   ├── main.py                # FastAPI entry point
│   ├── routes.py              # API routes
│   ├── services/              # Business logic layer
│   │   ├── detection.py       # Object detection logic
│   │   └── log_manager.py     # Logging & summary handling
│   ├── static/                # Static assets (CSS, JS, images)
│   └── templates/             # Jinja2 templates (HTML UI)
│
│── requirements.txt           # Python dependencies
│── Dockerfile                 # Container setup
│── docker-compose.yml         # Optional (for local dev)
│── .dockerignore              # Ignore files in Docker builds
│
│── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI/CD pipeline
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/smart_inventory.git
cd smart_inventory
```

### 2️⃣ Create a virtual environment
```bash
python -m venv visionenv
source visionenv/bin/activate   # Linux/Mac
visionenv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the App

### Development (hot reload)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access at:
- Local: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- Network: `http://<your-ip>:8000`

---

## 🐳 Docker Setup

### Build image
```bash
docker build -t smart-inventory .
```

### Run container
```bash
docker run -p 8000:8000 smart-inventory
```

---

## ✅ API Endpoints

- `GET /` — Render index page.  
- `POST /detect` — Upload an image for detection.  

Example (using `curl`):
```bash
curl -X POST -F "file=@sample.jpg" http://127.0.0.1:8000/detect
```

---

## 🔄 CI/CD

This project includes a **GitHub Actions workflow**:
- Linting and formatting checks.
- Build and test automation.
- Docker build validation.

Workflow file: `.github/workflows/ci.yml`

---

## 📌 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — Web framework.
- [Uvicorn](https://www.uvicorn.org/) — ASGI server.
- [Jinja2](https://jinja.palletsprojects.com/) — HTML templating.
- [PyTorch / Transformers](https://huggingface.co/) — AI models.
- [Docker](https://www.docker.com/) — Containerization.

---

## 🤝 Contributing

1. Fork the repo  
2. Create a new branch (`feature/your-feature`)  
3. Commit changes with clear messages  
4. Push to your branch and create a Pull Request  

---

## 📜 License

MIT License © 2025 [Your Name]

---
