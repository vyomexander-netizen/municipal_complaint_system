import streamlit as st
import plotly.express as px

from api_calls import (
    citizen_register,
    citizen_login,
    authority_register,
    authority_login,
    complaint_submission,
    get_my_complaints,
    get_authority_complaints,
    update_complaint_status,
    get_authority_analytics,
    update_complaint_department,
)
def get_error_message(response, default_message):
    try:
        return response.json().get("detail", default_message)
    except Exception:
        return response.text or default_message
def apply_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #071426 0%, #0b1f3a 45%, #102a4c 100%);
            color: #eaf2ff;
        }

        [data-testid="stSidebar"] {
            background: #06111f;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] * {
            color: #eaf2ff;
        }

        h1, h2, h3 {
            color: #ffffff;
            font-weight: 700;
        }

        .stButton > button {
            background: #1d4ed8;
            color: white;
            border: 1px solid #3b82f6;
            border-radius: 8px;
            padding: 0.55rem 1rem;
            font-weight: 600;
        }

        .stButton > button:hover {
            background: #2563eb;
            border-color: #60a5fa;
            color: white;
        }

        input, textarea, select {
            background-color: #0f2747 !important;
            color: #ffffff !important;
            border: 1px solid #315a89 !important;
            border-radius: 8px !important;
        }

        [data-testid="stTextInput"] label,
        [data-testid="stTextArea"] label,
        [data-testid="stSelectbox"] label {
            color: #cfe3ff !important;
            font-weight: 600;
        }

        [data-testid="stMetric"] {
            background: rgba(15, 39, 71, 0.85);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 8px;
            padding: 1rem;
        }

        [data-testid="stMetric"] * {
            color: #ffffff !important;
        }

        .stAlert {
            border-radius: 8px;
        }

        hr {
            border-color: rgba(255, 255, 255, 0.12);
        }

        [data-testid="stVerticalBlock"] {
            gap: 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show_citizen_register():
    st.subheader("Citizen Registration")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not username.strip() or not email.strip() or not password.strip():
            st.warning("Please fill all fields")
            return

        with st.spinner("Creating your account..."):
            response = citizen_register(username, email, password)

        if response.status_code == 200:
            st.success("Registration successful. Please login now.")
        else:
            st.warning(get_error_message(response, "Registration failed. Please try again."))

def show_citizen_login():
    if st.session_state.get("citizen_logged_in"):
        citizen_dashboard()
        return

    st.subheader("Citizen Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("login"):
        if not email.strip() or not password.strip():
            st.warning("Please enter email and password")
            return

        with st.spinner("Logging you in..."):
            response = citizen_login(email, password)

        if response.status_code == 200:
            data = response.json()
            st.session_state.citizen_token = data["access_token"]
            st.session_state.citizen_logged_in = True
            st.success("Login successful")
            citizen_dashboard()
        else:
            st.warning(get_error_message(response, "Login failed. Please check your details."))


def citizen_dashboard():
    st.subheader("Citizen Dashboard")

    if st.button("Logout", key="citizen_logout"):
        st.session_state.citizen_logged_in = False
        st.session_state.citizen_token = None
        st.session_state.citizen_dashboard_option = None
        st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Submit Complaint"):
            st.session_state.citizen_dashboard_option = "submit"

    with col2:
        if st.button("My Complaints"):
            st.session_state.citizen_dashboard_option = "my_complaints"

    if "citizen_dashboard_option" not in st.session_state:
        st.session_state.citizen_dashboard_option = None

    if st.session_state.citizen_dashboard_option == "submit":
        st.subheader("Submit Complaint")

        content = st.text_area("Complaint Description")
        location = st.text_input("Location")

        if st.button("Submit"):
            if not content.strip() or not location.strip():
                st.warning("Please enter complaint description and location")
                return

            with st.spinner("Submitting your complaint..."):
                response = complaint_submission(
                    content,
                    location,
                    st.session_state.citizen_token
                )

            if response.status_code == 200:
                data = response.json()

                st.success("Complaint submitted successfully")
                st.info(f"Complaint ID: {data['complaint_id']}")
            else:
                st.warning(get_error_message(response, "Complaint submission failed. Please try again."))

    elif st.session_state.citizen_dashboard_option == "my_complaints":
        with st.spinner("Loading your complaints..."):
            response = get_my_complaints(st.session_state.citizen_token)

        if response.status_code == 200:
            complaints = response.json()["complaints"]

            if not complaints:
                st.info("You have not submitted any complaints yet.")
                return

            for complaint in complaints:
                st.write("Complaint ID:", complaint["id"])
                st.write("Content:", complaint["content"])
                st.write("Location:", complaint["location"])
                st.write("Department:", complaint["department"])
                st.write("Urgency:", complaint["urgency"])
                st.write("Status:", complaint["status"])
                st.write("Created At:", complaint["created_at"])
                st.divider()
        else:
            st.warning("We could not load your complaints right now. Please try again.")


def show_authority_register():
    st.subheader("Authority Registration")

    username = st.text_input("Username", key="authority_register_username")
    email = st.text_input("Email", key="authority_register_email")
    department = st.selectbox(
    "Department",
    [
        "Roads",
        "Water",
        "Waste",
        "Electricity",
        "Public Safety"
    ],
    key="authority_register_department"
)
    


   
    password = st.text_input(
        "Password",
        type="password",
        key="authority_register_password"
    )
    security_code = st.text_input(
        "Security Code",
        key="authority_register_security_code"
    )

    if st.button("Register", key="authority_register_button"):
        if not username.strip() or not email.strip() or not password.strip() or not security_code.strip():
            st.error("Please fill all fields")
            return

        with st.spinner("Creating authority account..."):
         response = authority_register(
        username,
        email,
        password,
        department,
        security_code
    )

        if response.status_code == 200:
            st.success("Registration successful. Please login now.")
        else:
            st.error(get_error_message(response, "Registration failed"))


def show_authority_login():
    if st.session_state.get("authority_logged_in"):
        authority_dashboard(st.session_state.authority_token)
        return

    st.subheader("Authority Login")

    email = st.text_input("Email", key="authority_login_email")
    password = st.text_input(
        "Password",
        type="password",
        key="authority_login_password"
    )

    if st.button("Login", key="authority_login_button"):
        if not email.strip() or not password.strip():
            st.error("Please enter email and password")
            return
        with st.spinner("Logging you in..."):
         response = authority_login(email, password)

        if response.status_code == 200:
            data = response.json()
            st.session_state.authority_token = data["access_token"]
            st.session_state.authority_logged_in = True
            st.success("Login successful")
            authority_dashboard(st.session_state.authority_token)
        else:
            st.error(get_error_message(response, "Login failed"))


def authority_dashboard(token):
    st.subheader("Authority Dashboard")
    if st.button("Logout", key="authority_logout"):
     st.session_state.authority_logged_in = False
     st.session_state.authority_token = None
     st.session_state.transfer_complaint_id = None
     st.rerun()

    with st.spinner("Loading department analytics..."):
     analytics_response = get_authority_analytics(token)
    if analytics_response.status_code == 200:
        analytics = analytics_response.json()

        st.metric("Total Complaints", analytics["total_complaints"])

        
        

        urgency_data = analytics["by_urgency"]
        urgency_fig = px.pie(
            names=list(urgency_data.keys()),
            values=list(urgency_data.values()),
            title="Complaints by Urgency"
        )
        st.plotly_chart(urgency_fig)

        status_data = analytics["by_status"]
        status_fig = px.pie(
            names=list(status_data.keys()),
            values=list(status_data.values()),
            title="Complaints by Status"
        )
        st.plotly_chart(status_fig)
    else:
        st.error("Could not fetch analytics")

   

    urgency = st.selectbox(
        "Select Urgency",
        ["normal", "urgent", "critical"]
    )

    with st.spinner("Loading complaints..."):
     response = get_authority_complaints(token, urgency)

    
    
     if response.status_code == 200:
      complaints = response.json()

    if not complaints:
        st.info("No complaints found for this urgency.")

    for complaint in complaints:
            st.write("Complaint ID:", complaint["id"])

            if st.button("Transfer Department", key=f"show_transfer_{complaint['id']}"):
                st.session_state.transfer_complaint_id = complaint["id"]

            if st.session_state.get("transfer_complaint_id") == complaint["id"]:
                new_department = st.selectbox(
                    "Select New Department",
                    ["Roads", "Water", "Waste", "Electricity", "Public Safety"],
                    key=f"transfer_department_{complaint['id']}"
                )

                if st.button("Confirm Transfer", key=f"confirm_transfer_{complaint['id']}"):
                    with st.spinner("Transferring complaint..."):
                     transfer_response = update_complaint_department(
                        token,
                        complaint["id"],
                        new_department
                    )

                    if transfer_response.status_code == 200:
                        st.success("Department transferred")
                        st.session_state.transfer_complaint_id = None
                        st.rerun()
                    else:
                        st.error("Could not transfer department")

            st.write("Content:", complaint["content"])
            st.write("Location:", complaint["location"])
            st.write("Status:", complaint["status"])
            st.write("Created At:", complaint["created_at"])

            new_status = st.selectbox(
                "Update Status",
                ["submitted", "in_progress", "resolved"],
                key=f"status_{complaint['id']}"
            )

            if st.button("Update", key=f"update_{complaint['id']}"):
                with st.spinner("Updating status..."):
                 update_response = update_complaint_status(
                    token,
                    complaint["id"],
                    new_status
                )

                if update_response.status_code == 200:
                    st.success("Status updated")
                else:
                    st.error("Could not update status")

            st.divider()
    else:
        st.error("Could not fetch complaints")

apply_theme()
st.title("Municipal Complaint System")

option = st.sidebar.selectbox(
    "Choose Option",
    [
        "Citizen Register",
        "Citizen Login",
        "Authority Register",
        "Authority Login"
    ]
)

if option == "Citizen Register":
    show_citizen_register()

elif option == "Citizen Login":
    show_citizen_login()

elif option == "Authority Register":
    show_authority_register()

elif option == "Authority Login":
    show_authority_login()
