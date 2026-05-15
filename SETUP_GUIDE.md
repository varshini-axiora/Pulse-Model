# Team Setup Guide: AI Survey Generation System

Follow these steps to get the project running on your local machine after cloning.

## 1. Install & Start Ollama
This project requires a local LLM to function.
1.  **Download Ollama**: [https://ollama.com/download](https://ollama.com/download)
2.  **Pull the Model**: Open your terminal and run:
    ```bash
    ollama run phi3
    ```
    *Keep this running or ensure the Ollama service is active.*

## 2. Environment Setup
Clone the repository and navigate into the folder.

### Create Virtual Environment
```bash
# Create the environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (Mac/Linux)
# source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 3. Configuration (.env)
Create a file named `.env` in the root directory and add the following configuration:
```text
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3
DATABASE_URL=sqlite:///./survey_system.db
LOG_LEVEL=INFO
DEBUG=True
```

## 4. Run the Application

### Start the Backend
```bash
python -m uvicorn backend.app:app --reload
```
The API will be available at `http://localhost:8000`.

### Open the UI
Simply open `frontend/index.html` in your web browser.

## Troubleshooting
- **Ollama Connection Error**: Check if `http://localhost:11434` is accessible in your browser.
- **Missing Dependencies**: Ensure you are inside the virtual environment (`venv`) when running the backend.
- **Port Conflict**: If port 8000 is busy, run uvicorn with `--port 8001`.
