---
title: Municipal Complaint Backend
emoji: 🏛️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# AI-Powered Municipal Complaint System

A full-stack complaint-management platform that helps citizens report municipal issues and enables authorities to review, transfer, track, and resolve them.

The system uses two DistilBERT text-classification models to automatically:

- Route each complaint to the appropriate municipal department
- Assign an urgency level of `normal`, `urgent`, or `critical`

## Features

### Citizen portal

- Citizen registration and login
- Secure JWT-based authentication
- Complaint submission with description and location
- Automatic department and urgency classification
- Personal complaint history
- Live complaint-status tracking

### Authority portal

- Department-specific authority registration
- Registration-code verification
- Secure authority login
- Complaints filtered by department and urgency
- Status updates: `submitted`, `in_progress`, and `resolved`
- Complaint transfers between departments
- Department analytics with urgency and status charts

### Security

- Password hashing with bcrypt
- Role-based access for citizens and authorities
- JWT access tokens with a 30-minute expiry
- Department-level authorization for authority actions
- Environment-based secrets and database configuration

## Tech Stack

| Layer | Technologies |
| --- | --- |
| Frontend | Streamlit, Plotly, Requests |
| Backend | FastAPI, Uvicorn, Pydantic |
| Database | PostgreSQL, Psycopg |
| Authentication | JWT, Passlib, bcrypt |
| Machine learning | Transformers, DistilBERT, PyTorch |
| Training | Hugging Face Datasets, pandas, scikit-learn |
| Deployment | Docker, Hugging Face Spaces |

## Project Structure

```text
municipal/
├── backend/
│   ├── routers/
│   │   ├── authentication.py
│   │   ├── authorities.py
│   │   ├── complaints_tracking.py
│   │   └── security.py
│   ├── db_manager.py
│   ├── main.py
│   └── schemas.py
├── frontend/
│   ├── api_calls.py
│   ├── app.py
│   └── requirements.txt
├── model/
│   ├── classify_complaint.py
│   ├── classify_urgency.py
│   ├── train_model_classifcation.py
│   ├── train_model_urgency.py
│   ├── complaints.csv
│   └── urgency_complaints.csv
├── Dockerfile
├── requirements.txt
└── README.md
```

## How It Works

1. A citizen creates an account and logs in.
2. The citizen submits a complaint description and location.
3. The department model classifies the issue as one of:
   - Roads
   - Water
   - Waste
   - Electricity
   - Public Safety
4. The urgency model classifies it as `normal`, `urgent`, or `critical`.
5. The complaint is saved in PostgreSQL and shown to the relevant authority.
6. An authority can update its status or transfer it to another department.
7. The citizen can track the latest status from their dashboard.

## Local Setup

### Prerequisites

- Python 3.11
- PostgreSQL
- Two compatible Hugging Face text-classification models

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd municipal
```

### 2. Create and activate a virtual environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install backend dependencies

Install PyTorch using the command recommended for your system at
[pytorch.org](https://pytorch.org/get-started/locally/), then run:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/municipal
SECRET_KEY=replace-with-a-long-random-secret

DEPARTMENT_MODEL_ID=your-hugging-face-department-model
URGENCY_MODEL_ID=your-hugging-face-urgency-model

ROADS_AUTHORITY_CODE=roads-secret-code
WATER_AUTHORITY_CODE=water-secret-code
WASTE_AUTHORITY_CODE=waste-secret-code
ELECTRICITY_AUTHORITY_CODE=electricity-secret-code
PUBLIC_SAFETY_AUTHORITY_CODE=public-safety-secret-code
```

Do not commit the `.env` file or real authority registration codes.

### 5. Start the backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

- API: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

The required database tables are created automatically when the backend starts.

### 6. Connect and start the frontend

For local development, change `BASE_URL` in `frontend/api_calls.py` to:

```python
BASE_URL = "http://127.0.0.1:8000"
```

Install the frontend dependencies and launch Streamlit:

```bash
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

## API Endpoints

| Method | Endpoint | Access | Purpose |
| --- | --- | --- | --- |
| POST | `/citizencreate` | Public | Register a citizen |
| POST | `/citizenlogin` | Public | Log in as a citizen |
| POST | `/authoritycreate` | Public with registration code | Register an authority |
| POST | `/authoritylogin` | Public | Log in as an authority |
| POST | `/complaintsubmission` | Citizen | Submit and classify a complaint |
| GET | `/checkmycomplaints` | Citizen | View the citizen's complaints |
| GET | `/checkcomplaints?urgency=...` | Authority | View department complaints |
| PUT | `/updatestatus` | Authority | Update a complaint's status |
| PUT | `/updatedepartment` | Authority | Transfer a complaint |
| GET | `/authorityanalytics` | Authority | View department analytics |

Protected routes require the following header:

```http
Authorization: Bearer <access_token>
```

## Training the Models

The training scripts use `distilbert/distilbert-base-uncased`.

Department classifier:

```bash
cd model
python train_model_classifcation.py
```

Urgency classifier:

```bash
cd model
python train_model_urgency.py
```

The scripts split their CSV datasets into training, validation, and test sets. Trained models are saved under `model/saved_models/`.

## Docker

Build and run the backend:

```bash
docker build -t municipal-complaint-backend .
docker run --env-file .env -p 7860:7860 municipal-complaint-backend
```

The container serves the API on `http://localhost:7860`.

## Future Improvements

- Email or SMS status notifications
- Complaint evidence uploads
- Map-based complaint locations
- Automated escalation for overdue complaints
- Search, date filters, and downloadable reports
- Automated backend and frontend tests
- Administrator account for managing authorities

## Author

Developed as an AI-assisted municipal complaint routing and tracking project.
