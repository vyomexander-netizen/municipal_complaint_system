from backend.routers import authorities
from fastapi import FastAPI
from backend.db_manager import initialize_database

from backend.routers import complaints_tracking


from backend.routers.authentication import router as auth_router

app = FastAPI()
initialize_database()
app.include_router(auth_router)
app.include_router(authorities.router)
app.include_router(complaints_tracking.router)


    