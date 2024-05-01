# from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Form
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# from sqlalchemy.orm import Session
# from . import crud, models, schemas, database
# from .database import SessionLocal
# from .models import User

# app = FastAPI(title="Financial Exchange API", version="1.0.0", description="API for managing financial transactions")
# templates = Jinja2Templates(directory="templates")

# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.post("/users/", response_class=HTMLResponse)
# def create_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == username).first()
#     if db_user:
#         return HTMLResponse(content=f"<html><body><h1>Error: Username {username} already registered</h1></body></html>", status_code=400)
#     new_user = User(username=username, hashed_password=password)  # Simulate password hashing
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return HTMLResponse(content=f"<html><body><h1>User {username} created with ID: {new_user.id}</h1></body></html>", status_code=201)

# @app.get("/users/", response_class=HTMLResponse)
# def read_users(db: Session = Depends(get_db)):
#     users = db.query(User).all()
#     user_list = "".join(f"<li>{user.username} (ID: {user.id})</li>" for user in users)
#     return HTMLResponse(content=f"<html><body><h1>List of Users</h1><ul>{user_list}</ul></body></html>")

# @app.get("/users/{user_id}", response_class=HTMLResponse)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id)
#     if db_user is None:
#         return HTMLResponse(content="<html><body><h1>Error: User not found</h1></body></html>", status_code=404)
#     user_info = f"<h1>User Details</h1><ul>" \
#                 f"<li>Username: {db_user.username}</li>" \
#                 f"<li>User ID: {db_user.id}</li>" \
#                 f"<li>Admin Status: {'Yes' if db_user.is_admin else 'No'}</li>" \
#                 "</ul>"
#     return HTMLResponse(content=f"<html><body>{user_info}</body></html>")

# @app.put("/users/{user_id}", response_class=HTMLResponse)
# def update_user(user_id: int, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         return HTMLResponse(content="<html><body><h1>Error: User not found</h1></body></html>", status_code=404)
#     user.username = username
#     user.hashed_password = password  # Simulate password hashing
#     db.commit()
#     return HTMLResponse(content=f"<html><body><h1>User {user_id} updated</h1></body></html>")

# @app.delete("/users/{user_id}", response_class=HTMLResponse)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         return HTMLResponse(content="<html><body><h1>Error: User not found</h1></body></html>", status_code=404)
#     db.delete(user)
#     db.commit()
#     return HTMLResponse(content=f"<html><body><h1>User {user_id} deleted</h1></body></html>")


from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from .database import MONGO_URL
import uuid  # UUID generator

app = FastAPI(title="Financial Exchange API", version="1.0.0", description="API for managing financial transactions")

client = MongoClient(MONGO_URL)
db = client.financial_exchange  # Access the database
users_collection = db.users     # Access the users collection

class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False  # Default value for new users

class UserUpdate(BaseModel):
    username: str
    password: str
    is_admin: bool

def get_next_sequence(name):
    result = db.sequences.find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return result['seq']


@app.post("/users/", response_class=HTMLResponse)
def create_user(user: UserCreate):
    if users_collection.find_one({"username": user.username}):
        return HTMLResponse(content="<html><body><h1>Error: Username already registered</h1></body></html>", status_code=400)
    
    user_id = get_next_sequence("user_id")  # Assuming this function correctly returns an incrementing integer

    users_collection.insert_one({
        "id": user_id,
        "username": user.username,
        "hashed_password": user.password,  # This should be hashed securely
        "is_admin": user.is_admin
    })

    return HTMLResponse(content=f"<html><body><h1>User {user.username} successfully created with ID {user_id}.</h1></body></html>", status_code=201)


@app.get("/users/", response_class=HTMLResponse)
def read_users():
    users = list(users_collection.find({}, {"_id": 0, "username": 1, "id": 1, "is_admin": 1}))
    user_list = "<ul>"
    for user in users:
        username = user.get('username', 'No username')
        user_id = user.get('id', 'No ID')
        is_admin = 'Yes' if user.get('is_admin', False) else 'No'
        user_list += f"<li>{username} (ID: {user_id} - Admin: {is_admin})</li>"
    user_list += "</ul>"
    return HTMLResponse(content=f"<html><body><h1>List of Users</h1>{user_list}</body></html>")



@app.get("/users/{user_id}", response_class=HTMLResponse)
def read_user(user_id: int = Path(..., title="The ID of the user to retrieve")):
    user = users_collection.find_one({"id": user_id}, {"_id": 0})
    if not user:
        return HTMLResponse(content="<html><body><h1>Error: User not found</h1></body></html>", status_code=404)
    
    user_info = (
        f"<h1>User Details</h1><ul>"
        f"<li>Username: {user['username']}</li>"
        f"<li>User ID: {user['id']}</li>"
        f"<li>Admin Status: {'Yes' if user['is_admin'] else 'No'}</li>"
        "</ul>"
    )
    return HTMLResponse(content=f"<html><body>{user_info}</body></html>")


@app.put("/users/{user_id}", response_class=HTMLResponse)
def update_user(user_id: int, user: UserUpdate):
    result = users_collection.update_one(
        {"id": user_id},
        {"$set": {"username": user.username, "hashed_password": user.password, "is_admin": user.is_admin}}
    )
    if result.modified_count == 0:
        return HTMLResponse(content="<html><body><h1>Error: User not found or no update made.</h1></body></html>", status_code=404)

    return HTMLResponse(content=f"<html><body><h1>User {user_id} successfully updated.</h1></body></html>")

@app.delete("/users/{user_id}", response_class=HTMLResponse)
def delete_user(user_id: int):
    result = users_collection.delete_one({"id": user_id})
    if result.deleted_count == 0:
        return HTMLResponse(content="<html><body><h1>Error: User not found.</h1></body></html>", status_code=404)

    return HTMLResponse(content=f"<html><body><h1>User {user_id} successfully deleted.</h1></body></html>")


# @app.post("/users/", response_class=HTMLResponse)
# def create_user(user: UserCreate):
#     try:
#         with conn_pool.connection() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("SELECT * FROM users WHERE username = %s", (user.username,))
#                 if cur.fetchone() is not None:
#                     return HTMLResponse(content="<html><body><h1>Error: Username already registered</h1></body></html>", status_code=400)
                
#                 cur.execute("INSERT INTO users (username, hashed_password) VALUES (%s, crypt(%s, gen_salt('bf')))", (user.username, user.password))
#                 conn.commit()
#         return HTMLResponse(content=f"<html><body><h1>User {user.username} successfully created.</h1></body></html>", status_code=201)
#     except errors.UniqueViolation as e:
#         return HTMLResponse(content=f"<html><body><h1>Error: User ID already exists.</h1></body></html>", status_code=400)
#     except Exception as e:
#         return HTMLResponse(content=f"<html><body><h1>Server Error: {str(e)}</h1></body></html>", status_code=500)

# @app.get("/users/", response_class=HTMLResponse)
# def read_users():
#     with conn_pool.connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("SELECT id, username FROM users")
#             users = cur.fetchall()
#             user_list = "<ul>" + "".join(f"<li>{user[1]} (ID: {user[0]})</li>" for user in users) + "</ul>"
#     return HTMLResponse(content=f"<html><body><h1>List of Users</h1>{user_list}</body></html>")

# @app.get("/users/{user_id}", response_class=HTMLResponse)
# def read_user(user_id: int = Path(..., title="The ID of the user to retrieve")):
#     with conn_pool.connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("SELECT username, id, is_admin FROM users WHERE id = %s", (user_id,))
#             user = cur.fetchone()
#             if not user:
#                 return HTMLResponse(content="<html><body><h1>Error: User not found</h1></body></html>", status_code=404)
            
#             username, user_id, is_admin = user
#             user_info = (
#                 f"<h1>User Details</h1><ul>"
#                 f"<li>Username: {username}</li>"
#                 f"<li>User ID: {user_id}</li>"
#                 f"<li>Admin Status: {'Yes' if is_admin else 'No'}</li>"
#                 "</ul>"
#             )
#     return HTMLResponse(content=f"<html><body>{user_info}</body></html>")

# @app.put("/users/{user_id}", response_class=HTMLResponse)
# def update_user(user_id: int, user: UserUpdate):
#     with conn_pool.connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("UPDATE users SET username = %s, hashed_password = crypt(%s, gen_salt('bf')) WHERE id = %s", (user.username, user.password, user_id))
#             if cur.rowcount == 0:
#                 return HTMLResponse(content="<html><body><h1>Error: User not found or no update made.</h1></body></html>", status_code=404)
#             conn.commit()
    
#     return HTMLResponse(content=f"<html><body><h1>User {user_id} successfully updated.</h1></body></html>")

# @app.delete("/users/{user_id}", response_class=HTMLResponse)
# def delete_user(user_id: int):
#     with conn_pool.connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
#             if cur.rowcount == 0:
#                 return HTMLResponse(content="<html><body><h1>Error: User not found.</h1></body></html>", status_code=404)
#             conn.commit()
    
#     return HTMLResponse(content=f"<html><body><h1>User {user_id} successfully deleted.</h1></body></html>")

