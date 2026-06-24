# AI-Powered Municipal Complaint System

## What It Does

This project allows citizens to submit and track municipal complaints through
a web application.

It automatically analyzes each complaint using machine-learning models to:

- Send it to the appropriate department: Roads, Water, Waste, Electricity, or
  Public Safety
- Classify its urgency as normal, urgent, or critical

Citizens can view the status of their submitted complaints. Municipal
authorities can view complaints assigned to their department, update complaint
statuses, transfer complaints to another department, and view complaint
analytics.

## Tech Stack

- **Frontend:** Streamlit, Plotly
- **Backend:** FastAPI, Uvicorn
- **Database:** PostgreSQL, Psycopg
- **Machine learning:** DistilBERT, Hugging Face Transformers, PyTorch
- **Authentication:** JWT, Passlib, bcrypt
- **Data processing and training:** pandas, scikit-learn, Hugging Face Datasets
- **Deployment:** Docker, Hugging Face Spaces
