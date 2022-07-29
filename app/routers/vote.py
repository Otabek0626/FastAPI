from fastapi import FastAPI, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import utils, schemas, database, models, oauth2


router = APIRouter(
    prefix="/vote",
    tags=["Votes"])


@router.post("/", status_code=201)
async def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post id: {vote.post_id} was not found")

    query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=409, detail=f"user id: {current_user.id} has already voted to post id: {vote.post_id}")
        
        new_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "voted"}
        
    else:
        if not found_vote:
            raise HTTPException(status_code=409, detail=f"Vote does not exist")
        query.delete(synchronize_session=False)
        db.commit()
        return {"message": "vote deleted"}