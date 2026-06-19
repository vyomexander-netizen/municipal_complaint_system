
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from backend.schemas import ComplaintSubmission
from backend.routers.security import security, get_current_user
from backend.db_manager import get_user_by_email, insert_general_complaint, get_complaints_by_citizen_id
from model.classify_complaint import classify_complaint
from model.classify_urgency import classify_urgency

router = APIRouter()

@router.post("/complaintsubmission")
def submit_complaint(
    complaint: ComplaintSubmission,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)

    if current_user["role"] != "citizen":
        raise HTTPException(
            status_code=403,
            detail="Only citizens can submit complaints"
        )
    if not complaint.content.strip() or not complaint.location.strip():
     raise HTTPException(
        status_code=400,
        detail="Complaint content and location are required"
    )

    email = current_user["email"]
    stored_user = get_user_by_email(email)

    if stored_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid user"
        )

    citizen_id = stored_user[0]

    department = classify_complaint(complaint.content)
    urgency = classify_urgency(complaint.content)

    complaint_id = insert_general_complaint(
        citizen_id=citizen_id,
        content=complaint.content,
        location=complaint.location,
        department=department,
        urgency=urgency
    )

    return {
        "message": "Complaint submitted successfully",
        "complaint_id": complaint_id,
        "department": department,
        "urgency": urgency,
        "status": "submitted"
    }


@router.get("/checkmycomplaints")
def check_my_complaints(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)

    if current_user["role"] != "citizen":
        raise HTTPException(
            status_code=403,
            detail="Only citizens can view their complaints"
        )

    email = current_user["email"]
    stored_user = get_user_by_email(email)

    if stored_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid user"
        )

    citizen_id = stored_user[0]
    complaints = get_complaints_by_citizen_id(citizen_id)

    return {
        "complaints": complaints
    }

    
