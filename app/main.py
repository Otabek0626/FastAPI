from typing import List
from fastapi import FastAPI, HTTPException, Response, Depends

from sqlalchemy.orm import Session

from .routers import post, user, auth, vote
from . import models, database
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


origins = [
    "https://www.google.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=database.engine)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
async def main():
    return {"message": "mmmm"}