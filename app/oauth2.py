from jose import JWTError, jwt
from datetime import datetime, timedelta
from routers import auth
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import *
from sqlalchemy.orm import Session
from config import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = auth.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oath2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate crentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(Student).filter(Student.id == token.id).first()

    if not user:
        user = db.query(Teacher).filter(Teacher.id == token.id).first()
    
    elif not user:
        user = db.query(Parent).filter(Parent.id == token.id).first()
    
    elif not user:
        user = db.query(Admin).filter(Admin.id == token.id).first()
    
    return user
