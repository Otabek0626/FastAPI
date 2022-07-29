from fastapi import FastAPI, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import utils, schemas, database, models, oauth2

from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"])

@router.post("/", status_code=201, response_model = schemas.PostOut)
async def create_post(post: schemas.Post, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model = List[schemas.PostVoteOut])
async def get_posts(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.title.contains(search)).group_by(models.Post.id).limit(limit).all()
    return posts

@router.get("/{id}", response_model = schemas.PostOut)
async def get_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found!")
    return post
    

@router.put("/{id}", status_code=201)
async def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found!")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Post with ID: {id} is not belong to this user")

    query.update({**updated_post.dict()}, synchronize_session = False)
    db.commit()
    return Response(status_code=201)
    
@router.delete("/{id}", status_code=204)
async def delete_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found!")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Post with ID: {id} is not belong to this user")

    query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=204)

    