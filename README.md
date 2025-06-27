# 🖼️ Text-to-Image Microservice

A scalable microservice built with **FastAPI**, integrated with **OpenAI's image generation API** (or any compatible provider), deployed via **Docker** and **Terraform on GCP**.
This service accepts text prompts and returns generated image URLs.

---

## 🚀 Features

* 🔌 REST API with FastAPI (`POST /generate`)
* ⚡ Async HTTP calls via `httpx`
* 🔁 Retry logic with fallback using `tenacity`
* 📦 Containerized with Docker (multi-stage build)
* ☁️ Cloud-ready with Terraform for Google Cloud Run
* ✅ Unit tested with `pytest`, `httpx`, `tenacity`
* 🔧 Clean error handling, structured logging-ready

---

## 🥪 API Usage

### `POST /text-to-img`

**Request:**

```json
{
  "text": "a robot playing chess in space"
}
```

**Response:**

```json
{
  "url": "https://your-image-url.com/image.png"
}
```

Use the interactive docs at:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ⚙️ Local Development

### 1. Clone & Setup

```bash
git clone https://github.com/mahdinet1/text-to-image.git
cd text-to-image-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Locally

```bash
uvicorn app.main:app --reload
```

---

## 📣 Docker

### Build & Run

```bash
docker build -t text-to-image-service .
docker run -p 8000:8000 text-to-image-service
```

---

## ☁️ GCP Deployment with Terraform

### Prerequisites

* Enable GCP APIs: `run.googleapis.com`, `artifactregistry.googleapis.com`
* Docker image built & pushed to Artifact Registry

### Deploy with Terraform

```bash
cd deployment/IaC/terraform
terraform init
terraform plan
terraform apply 
```

After deploy, Terraform will output a live URL like:

```text
cloud_run_url = "https://text-to-image-xyz.a.run.app"
```

---

## 🥪 Running Tests

```bash
PYTHONPATH=. pytest test/
```

---

## 🔐 Environment Variables

Place these in a `.env` file or use Docker/Terraform env settings:

| Variable         | Description                  |
| ---------------- | ---------------------------- |
| `OPENAI_API_KEY` | API key for image generation |

---

## 📦 Dependencies

* `fastapi`
* `uvicorn[standard]`
* `httpx`
* `tenacity`
* `python-dotenv`
* `pytest`, `pytest-asyncio`

---
