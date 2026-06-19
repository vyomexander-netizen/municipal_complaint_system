from backend.routers.security import create_access_token
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from backend.routers.security import security, get_current_user

from backend.schemas import UserLogin, AuthorityCreate, StatusUpdate, DepartmentUpdate

from backend.db_manager import (
    is_authority_email_available,
    create_authority,
    get_authority_by_email,
    get_authorities_complaint,
    update_complaint_status,
    get_authority_analytics,
    updation_of_department,get_complaint_department
)


import os

from dotenv import load_dotenv

load_dotenv()


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
DEPARTMENT_CODES = {
    "Roads": os.getenv("ROADS_AUTHORITY_CODE"),
    "Water": os.getenv("WATER_AUTHORITY_CODE"),
    "Waste": os.getenv("WASTE_AUTHORITY_CODE"),
    "Electricity": os.getenv("ELECTRICITY_AUTHORITY_CODE"),
    "Public Safety": os.getenv("PUBLIC_SAFETY_AUTHORITY_CODE"),
}
VALID_DEPARTMENTS = [
    "Roads",
    "Water",
    "Waste",
    "Electricity",
    "Public Safety"
]

@router.post("/authoritycreate")
def register_authority(authority: AuthorityCreate):
    expected_code = DEPARTMENT_CODES.get(authority.department)

    if expected_code is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid department"
        )

    if authority.registration_code != expected_code:
        raise HTTPException(
            status_code=403,
            detail="Invalid authority registration code"
        )

    if not is_authority_email_available(authority.email):
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return create_authority(
        username=authority.username,
        email=authority.email,
        password=pwd_context.hash(authority.password),
        department=authority.department
    )



@router.post("/authoritylogin")
def login_user(user: UserLogin):
    stored_user = get_authority_by_email(user.email)

    if stored_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not pwd_context.verify(user.password, stored_user[2]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    access_token = create_access_token(
    data={
        "sub": user.email,
        "role": "authority",
        "department": stored_user[3]
    }
)

    

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/checkcomplaints")
def check_the_complaints(
    urgency: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)

    if current_user["role"] != "authority":
        raise HTTPException(
            status_code=403,
            detail="Only authorities can view complaints"
        )

    department = current_user["department"]
    complaint = get_authorities_complaint(department, urgency)

    return complaint


@router.put("/updatestatus")
def update_status(
    status: StatusUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)

    if current_user["role"] != "authority":
        raise HTTPException(
            status_code=403,
            detail="Only authorities can update complaint status"
        )

    if status.status not in ["submitted", "in_progress", "resolved"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    complaint_department = get_complaint_department(status.complaint_id)

    if complaint_department is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    if complaint_department != current_user["department"]:
        raise HTTPException(
            status_code=403,
            detail="You can only update complaints from your department"
        )

    updated = update_complaint_status(status.complaint_id, status.status)

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    return {
        "message": "Status updated successfully"
    }

    

@router.get("/authorityanalytics")
def authority_analytics(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)

    if current_user["role"] != "authority":
        raise HTTPException(
            status_code=403,
            detail="Only authorities can view analytics"
        )
    department = current_user["department"]
    return get_authority_analytics(department)






@router.put("/updatedepartment")
def update_the_department(
    update: DepartmentUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)

    if current_user["role"] != "authority":
        raise HTTPException(
            status_code=403,
            detail="Only authorities can update department"
        )

    complaint_department = get_complaint_department(update.complaint_id)

    if complaint_department is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    if complaint_department != current_user["department"]:
        raise HTTPException(
            status_code=403,
            detail="You can only transfer complaints from your department"
        )
    if update.department not in VALID_DEPARTMENTS:
     raise HTTPException(
        status_code=400,
        detail="Invalid target department"
    )

    updated = updation_of_department(update.complaint_id, update.department)

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    return {
        "message": "Department updated successfully"
    }