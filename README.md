# AI Survey Generation System (Local)

A production-quality survey generation system powered by **Microsoft Phi-3 Mini** running locally via **Ollama**. Optimized for CPU inference on standard laptops.

## Features
- **Local Inference**: Privacy-first, no external APIs required.
- **Input Cleaning**: Automatically corrects grammar and rephrases intent.
- **Intent Analysis**: Extracts audience, industry, and goals.
- **Semantic Validation**: Uses `sentence-transformers` to prevent duplicate or irrelevant questions.
- **Glassmorphism UI**: Modern, premium frontend experience.
- **SQLite Storage**: Keeps a history of generated surveys.

## Tech Stack
- **Backend**: FastAPI, Pydantic, SQLAlchemy
- **LLM**: Ollama (Phi-3 Mini)
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **Frontend**: Vanilla HTML/CSS/JS (Glassmorphism)

## Setup Instructions

### 1. Install Ollama
Download and install Ollama from [ollama.com](https://ollama.com/).

### 2. Pull the Phi-3 Model
Run the following command in your terminal:
```bash
ollama run phi3
```

### 3. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Backend
```bash
uvicorn backend.app:app --reload
```

### 6. Open the Frontend
Simply open `frontend/index.html` in your web browser.

## API Endpoints
- `POST /generate-survey`: Main entry point for survey creation.
- `POST /analyze-input`: Quick analysis of a raw text input.
- `GET /health`: Check status of the API and Ollama connection.

## Example Request
```json
{
  "raw_text": "i want a survey for my new mobile app that helps people track their water intake. i want to know if they like the UI and if they would pay for premium."
}
```

## Performance Note
Since this runs on CPU, the "Validating Quality" and "Generating Questions" steps may take 10-20 seconds. The UI provides real-time progress feedback.

## License
MIT
