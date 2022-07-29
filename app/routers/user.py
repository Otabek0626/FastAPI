from fastapi import FastAPI, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import utils, schemas, database, models, oauth2

router = APIRouter(
    prefix="/users",
    tags=["Users"])

@router.post("/", status_code=201, response_model = schemas.UserReturn)
async def user_create(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/posts", response_model = List[schemas.PostOut])
async def get_posts(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    return posts

@router.get("/{id}", response_model = schemas.UserReturn)
async def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"user with id: {id} was not found!")
    return user



