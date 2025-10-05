# app/routes/user_routes.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from auth.auth_handler import create_access_token, invalidate_token
from auth.auth_bearer import JWTBearer
from models import SignupRequest, LoginRequest

router = APIRouter(prefix="/auth/v1", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Temporary in-memory "user database"
users_db = {}

def hash_password(password: str) -> str:
    # Ensure we always pass in a plain string
    if not isinstance(password, str):
        password = password.decode("utf-8")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/signup")
def signup(request: SignupRequest):
    if request.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = hash_password(request.password)
    users_db[request.email] = {"password": hashed}
    return {"message": "User created successfully"}

@router.post("/login")
def login(request: LoginRequest):
    user = users_db.get(request.email)
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": request.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout", dependencies=[Depends(JWTBearer())])
def logout(token: str = Depends(JWTBearer())):
    # JWTBearer returns user email, so we need actual token from header
    # easiest is to re-parse from Authorization header in main
    invalidate_token(token)
    return {"message": "Logged out successfully"}
