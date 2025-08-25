# Basic-AI-based-Email-Generator
Generate emails depending on the category based on AI

## 📘 How to use it the system?

- Select the email category
- Enter the receiver's name, subject, and details.
- Click the "Generate Email" button to get your generated email.

## Category
- "Inquiry": You want information or clarification on a topic.
- "request": You are actively asking for something.
- "information": You inform someone neutrally about something.
- "confirmation": You confirm something in writing.
- "complaint": You report a problem or defect.
- "apology": You apologize for an oversight or problem.
- "reminder": You remind yourself of a deadline or task.
- "invitation": You invite someone to something.
- "other": You just want a simple email.
  

## Getting started

### 1. Install dependencies

  #### - pip install -r requirements.txt
    

### 2. Make sure you’ve got the following tools installed:

  #### - FastAPI

  #### - Streamlit

  #### - Ollama – for local LLM processing (e.g. with llama3)
    

### 3. Launch the backend

  #### - uvicorn backend:app --reload
    

### 4. Start Ollama

  #### - ollama run llama3
    

### 5. Run the frontend

  #### - streamlit run app.py
