import requests
BASE_URL = "https://niggachu21-municipal-complaint-backend.hf.space"



def citizen_register(username, email, password):
    response = requests.post(
        f"{BASE_URL}/citizencreate",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )

    return response

def citizen_login(email, password):
    response = requests.post(
        f"{BASE_URL}/citizenlogin",
        json={
            "email": email,
            "password": password
        }
    )

    return response

def authority_register(username, email, password,department, security_code):
    response = requests.post(
        f"{BASE_URL}/authoritycreate",
        json={
            "username": username,
            "email": email,
            "password": password,
            "department": department,
            "registration_code": security_code
        }
    )

    return response

def authority_login(email, password):
    response = requests.post(
        f"{BASE_URL}/authoritylogin",
        json={
            "email": email,
            "password": password
        }
    )

    return response



def complaint_submission(content, location, token):
    response = requests.post(
        f"{BASE_URL}/complaintsubmission",
        json={
            "content": content,
            "location": location
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


def get_my_complaints(token):
    response = requests.get(
        f"{BASE_URL}/checkmycomplaints",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response

def get_authority_complaints(token, urgency):
    response = requests.get(
        f"{BASE_URL}/checkcomplaints",
        headers={
            "Authorization": f"Bearer {token}"
        },
        params={
            "urgency": urgency
        }
    )

    return response




def update_complaint_status(token, complaint_id, new_status):
    response = requests.put(
        f"{BASE_URL}/updatestatus",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "complaint_id": complaint_id,
            "status": new_status
        }
    )

    return response


def get_authority_analytics(token):
    response = requests.get(
        f"{BASE_URL}/authorityanalytics",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


def update_complaint_department(token, id, department):
    response = requests.put(
        f"{BASE_URL}/updatedepartment",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "complaint_id": id,
            "department": department
        }
    )

    return response

    



