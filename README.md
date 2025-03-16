# LangChain Chatbot with OpenAI and FastAPI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)

A production-ready chatbot solution leveraging LangChain, OpenAI GPT, and FastAPI, designed for easy deployment on Render.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [FAQ Training](#faq-training)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features ✨
- **Custom FAQ Training** (PDF/TXT/CSV)
- **AI-Powered Responses** using OpenAI GPT
- **Vector Similarity Search** with FAISS
- **Docker Containerization**
- **Production-Ready API** with FastAPI
- **Health Check Endpoint**

## Prerequisites 👋
- Python 3.9+
- OpenAI API Key
- Docker (for containerization)
- Render Account (for deployment)

## Installation 🛠️

```bash
# Clone repository
git clone https://github.com/your-username/langchain-chatbot.git
cd langchain-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration ⚙️

1. Create `.env` file:
```bash
cp .env.example .env
```

2. Edit `.env`:
```env
OPENAI_API_KEY="your-openai-api-key"
```

3. Add FAQ documents to `app/faqs/` directory

## Usage 🚀

### Local Development
```bash
uvicorn app.main:app --reload
```

### Test API
```bash
# Health check
curl http://localhost:8000/health

# Ask question
curl -X POST "http://localhost:8000/ask" \
-H "Content-Type: application/json" \
-d '{"question": "What is your refund policy?"}'
```

## Deployment 🐳

### Docker Build
```bash
docker build -t langchain-chatbot .
```

### Docker Run
```bash
docker run -d -p 8000:8000 --env-file .env --name chatbot langchain-chatbot
```

### Render Deployment
1. Push code to GitHub
2. Create new Web Service on Render
3. Configure:
   - **Runtime**: Docker
   - **Port**: 8000
   - **Environment Variables**:
     - `OPENAI_API_KEY`: Your OpenAI key

## API Documentation 📚

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ask`   | POST   | Submit questions |
| `/health`| GET    | Service status |

### Request Example
```json
POST /ask
{
  "question": "How do I contact support?"
}
```

### Response Example
```json
{
  "answer": "Our support team can be reached 24/7 at support@company.com..."
}
```

## FAQ Training 📚

1. Add documents to `app/faqs/`
2. Supported formats:
   - PDF (`.pdf`)
   - Text (`.txt`)
   - CSV (`.csv`)
3. On application startup:
   - Automatic embedding generation
   - FAISS vector store update

## Troubleshooting 🔧

### Common Issues
1. **Missing OpenAI Key**
   - Verify `.env` file exists
   - Check Render environment variables

2. **PDF Loading Errors**
   - Ensure file is not password protected
   - Verify file integrity

3. **Docker Build Failures**
   - Clear Docker cache: `docker system prune -a`
   - Check network connectivity

## License 📝
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
