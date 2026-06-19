import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

def initialize_database():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS authorities (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    department TEXT NOT NULL
                );
            """)
            cur.execute("""
    ALTER TABLE authorities
    ADD COLUMN IF NOT EXISTS department TEXT;
""")

            cur.execute("""
                ALTER TABLE users
                DROP CONSTRAINT IF EXISTS users_username_key;
            """)

            cur.execute("""
                ALTER TABLE authorities
                DROP CONSTRAINT IF EXISTS authorities_username_key;
            """)

            cur.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS users_email_key
                ON users(email);
            """)

            cur.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS authorities_email_key
                ON authorities(email);
            """)

            cur.execute("""
    CREATE TABLE IF NOT EXISTS general_complaints (
        id SERIAL PRIMARY KEY,
        citizen_id INTEGER NOT NULL REFERENCES users(id),
        content TEXT NOT NULL,
        location TEXT NOT NULL,
        department TEXT NOT NULL,
        urgency TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'submitted',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

            

def is_email_available(email: str) -> bool:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM users WHERE email = %s",
                (email,)
            )
            return cur.fetchone() is None


        

def create_user(username: str, email: str, password: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            

            cur.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (username, email, password)
            )

            return cur.fetchone()[0]
        
def get_user_by_email(email: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, email, password
                FROM users
                WHERE email = %s
                """,
                (email,)
            )
            return cur.fetchone()

def is_authority_email_available(email: str) -> bool:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM authorities WHERE email = %s",
                (email,)
            )
            return cur.fetchone() is None
        
def create_authority(username: str, email: str, password: str,department: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            

            cur.execute(
                """
                INSERT INTO authorities (username, email, password,department)
                VALUES (%s, %s, %s,%s)
                RETURNING id;
                """,
                (username, email, password,department)
            )

            return cur.fetchone()[0]
        
def get_authority_by_email(email: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, email, password,department
                FROM authorities
                WHERE email = %s
                """,
                (email,)
            )
            return cur.fetchone()
        
        
        




def insert_general_complaint(
    citizen_id: int,
    content: str,
    location: str,
    department: str,
    urgency: str
):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO general_complaints
                (citizen_id, content, location, department, urgency)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (citizen_id, content, location, department, urgency)
            )

            return cur.fetchone()[0]
        
        


        
def get_complaints_by_citizen_id(citizen_id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, content, location, department, urgency, status, created_at
                FROM general_complaints
                WHERE citizen_id = %s
                ORDER BY created_at DESC;
                """,
                (citizen_id,)
            )

            rows = cur.fetchall()

            return [
                {
                    "id": row[0],
                    "content": row[1],
                    "location": row[2],
                    "department": row[3],
                    "urgency": row[4],
                    "status": row[5],
                    "created_at": str(row[6])
                }
                for row in rows
            ]
def get_authorities_complaint(department: str, urgency: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, citizen_id, content, location, department, urgency, status, created_at
                FROM general_complaints
                WHERE department = %s AND urgency = %s
                ORDER BY created_at DESC;
                """,
                (department, urgency)
            )

            rows = cur.fetchall()

            return [
                {
                    "id": row[0],
                    "citizen_id": row[1],
                    "content": row[2],
                    "location": row[3],
                    "department": row[4],
                    "urgency": row[5],
                    "status": row[6],
                    "created_at": str(row[7])
                }
                for row in rows
            ]

def update_complaint_status(complaint_id: int, status: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE general_complaints
                SET status = %s
                WHERE id = %s
                RETURNING id
                """,
                (status, complaint_id)
            )
            return cur.fetchone()

def get_authority_analytics(department: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, citizen_id, content, location, department, urgency, status, created_at
                FROM general_complaints
                WHERE department = %s
                ORDER BY created_at DESC;
                """,
                (department,)
            )

            rows = cur.fetchall()

            total_complaints = len(rows)

            by_urgency = {
                "normal": 0,
                "urgent": 0,
                "critical": 0
            }

            by_status = {
                "submitted": 0,
                "in_progress": 0,
                "resolved": 0
            }

            for row in rows:
                urgency = row[5]
                status = row[6]

                if urgency in by_urgency:
                    by_urgency[urgency] += 1

                if status in by_status:
                    by_status[status] += 1

            return {
                "total_complaints": total_complaints,
                "by_urgency": by_urgency,
                "by_status": by_status
            }
    

def updation_of_department(complaint_id,department):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE general_complaints
                SET department = %s
                WHERE id = %s
                RETURNING id
                """,
                (department, complaint_id)
            )
            return cur.fetchone()
        
def get_complaint_department(complaint_id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT department
                FROM general_complaints
                WHERE id = %s
                """,
                (complaint_id,)
            )

            row = cur.fetchone()

            if row is None:
                return None

            return row[0]


            

