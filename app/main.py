from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import *
from routers.utils import auth, user
from routers.general import schedule
from routers.admin import admintools
from routers.teacher import attendance

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]  # My domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utils
app.include_router(auth.router)
app.include_router(user.router)

# General
app.include_router(schedule.router)

# Teacher
app.include_router(attendance.router)

# Admin
app.include_router(admintools.router)



@app.get("/")
def root():
    return "test"