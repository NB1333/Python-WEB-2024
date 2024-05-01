from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from .database import SessionLocal
from .models import User

app = FastAPI(title="Financial Exchange API", version="1.0.0", description="API for managing financial transactions")
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_class=HTMLResponse)
def create_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        return HTMLResponse(content=f"<html><body><h1>Error: Username {username} already registered</h1></body></html>", status_code=400)
    new_user = User(username=username, hashed_password=password)  # Simulate password hashing
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return HTMLResponse(content=f"<html><body><h1>User {username} created with ID: {new_user.id}</h1></body></html>", status_code=201)

@app.get("/users/", response_class=HTMLResponse)
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    user_list = "".join(f"<li>{user.username} (ID: {user.id})</li>" for user in users)
    return HTMLResponse(content=f"<html><body><h1>List of Users</h1><ul>{user_list}</ul></body></html>")

@app.get("/users/{user_id}", response_class=HTMLResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        return HTMLResponse(content="<html><body><h1>Error: User not found</h1></body></html>", status_code=404)
    user_info = f"<h1>User Details</h1><ul>" \
                f"<li>Username: {db_user.username}</li>" \
                f"<li>User ID: {db_user.id}</li>" \
                f"<li>Admin Status: {'Yes' if db_user.is_admin else 'No'}</li>" \
                "</ul>"
    return HTMLResponse(content=f"<html><body>{user_info}</body></html>")

@app.put("/users/{user_id}", response_class=HTMLResponse)
def update_user(user_id: int, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse(content="<html><body><h1>Error: User not found</h1></body></html>", status_code=404)
    user.username = username
    user.hashed_password = password  # Simulate password hashing
    db.commit()
    return HTMLResponse(content=f"<html><body><h1>User {user_id} updated</h1></body></html>")

@app.delete("/users/{user_id}", response_class=HTMLResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse(content="<html><body><h1>Error: User not found</h1></body></html>", status_code=404)
    db.delete(user)
    db.commit()
    return HTMLResponse(content=f"<html><body><h1>User {user_id} deleted</h1></body></html>")