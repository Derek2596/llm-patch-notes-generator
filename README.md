# LLM App Project: Automated Patch Notes Generator

This project implements a small FastAPI application that leverages the Gemini API to transform unstructured, concise development bullet points into formatted, structured patch notes suitable for release documentation.

# Repro & Quick Start
Follow these steps to set up and run the application and the test suite locally.

### 1. Setup Environment
Clone the repository and install the dependencies:
```
git clone <your-repo-link>
cd <your-repo-name>
pip install -r requirements.txt
```
### 2. Configure Environment Variables
Create a .env file using the .env.example and replace YOUR_API_KEY with your actual Gemini API key.

```.env``` :
```
# Replace YOUR_API_KEY with your actual Gemini API key
GEMINI_API_KEY=YOUR_API_KEY
```

### 3. Run the FastAPI Service
Start the patch notes generator server using uvicorn.
```
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open the App
Go to [127.0.0.1:8000](127.0.0.1:8000) in your browser.