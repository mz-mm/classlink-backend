from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"] # My domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return "test"
