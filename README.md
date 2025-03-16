Here's a comprehensive `README.md` for your GitHub repository:

```markdown
# LangChain Chatbot

[![LangChain](https://img.shields.io/badge/LangChain-0.1.16-blue)](https://langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.14.2-brightgreen)](https://openai.com)
[![Docker](https://img.shields.io/badge/Docker-✓-blue)](https://docker.com)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46a3b7)](https://render.com)

A production-ready chatbot powered by LangChain and OpenAI GPT, featuring custom FAQ training and FastAPI backend.

## Features

- 🧠 GPT-3.5/4 powered responses
- 📚 Custom FAQ training (PDF/TXT/CSV)
- 🐳 Docker container support
- 🚀 FastAPI backend
- 🔍 FAISS vector similarity search
- 💻 Render deployment ready

## Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key
- Docker (optional)

### Installation

1. Clone repository:
```bash
git clone https://github.com/your-username/langchain-chatbot.git
cd langchain-chatbot
```

2. Set up environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

### Usage

1. Place FAQ documents in `app/faqs/`
2. Start the server:
```bash
uvicorn app.main:app --reload
```

3. Test API:
```bash
curl -X POST "http://localhost:8000/ask" \
-H "Content-Type: application/json" \
-d '{"question": "What is your return policy?"}'
```

## Deployment

### Docker Setup

1. Build image:
```bash
docker build -t langchain-chatbot .
```

2. Run container:
```bash
docker run -d -p 8000:8000 --env-file .env --name chatbot langchain-chatbot
```

### Render Deployment

1. Push to GitHub repository
2. Create new Web Service on [Render Dashboard](https://dashboard.render.com/)
3. Configure:
   - **Runtime**: Docker
   - **Port**: 8000
   - **Environment Variables**:
     - `OPENAI_API_KEY`: Your OpenAI key

## Configuration

### Environment Variables
```env
OPENAI_API_KEY=your-openai-key
```

### File Structure
```
.
├── app/
│   ├── faqs/          # Custom FAQ documents
│   ├── vector_store/  # Generated vector store
│   └── main.py        # FastAPI application
├── Dockerfile
├── requirements.txt
└── README.md
```

## API Documentation

### Endpoints
- `POST /ask`
  ```json
  {
    "question": "Your question here"
  }
  ```
  
- `GET /health`
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```

## Training Custom FAQ

1. Add documents to `app/faqs/`
2. Supported formats: PDF, TXT, CSV
3. The system automatically regenerates embeddings on startup

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add some feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open Pull Request

## License

MIT License
