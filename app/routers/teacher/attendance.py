from typing import Optional, List, Union
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import *
import oauth2 as oauth2


router = APIRouter(
    tags=["Teacher Attendance"]
)


@router.get("/api/attendence")
def mark_attendance(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    return {"result":"attendence"}


@router.post("/api/attendence")
def mark_attendance(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    return {"result":"mark attendence"}