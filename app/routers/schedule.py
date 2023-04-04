from typing import Optional, List
from fastapi import FastAPI, Response, HTTPException, status, Form, Depends, Body, APIRouter
from pydantic import BaseModel, EmailStr
from database import *
from sqlalchemy.orm import Session6
from datetime import datetime
import oauth2

router = APIRouter(
    tags=["Lesson"]
)

"""
Schedule fetching to the frontend

The process:
- Get the current user
- Get the current user's class id
- All the lessons with the class id
- Sort them by the day and lesson number, for example the first returned lesson will be the first lesson of the first day and so on
- Return the lessons 

The frontend will get all the lessons and then will display them through a nested loop, first the days and then the lessons
Then get the lessons name and color and display them

If the the user is on a mobile page, the frotend will have to make a quiry to the backend to get the lessons of the current day
"""


