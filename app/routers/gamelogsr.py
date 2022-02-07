from calendar import c
from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import Boolean, desc, true, text
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas, utils

router = APIRouter()


@router.get("/gamelogsr/checkhash/{changehash}", status_code=status.HTTP_200_OK)
def get_gameslogchangehash(changehash: str, db: Session = Depends(get_db)):

    
    gamelog = db.query(models.GameLogSR).filter(models.GameLogSR.changehash == changehash).first()

    if not gamelog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"log entry not found yet. You can post your entry now.")

    return gamelog


@router.post("/gamelogsr", status_code=status.HTTP_201_CREATED, response_model=schemas.GameLogSRBase)
def post_gamelogsr(gamelog: schemas.GameLogSRBase, db: Session = Depends(get_db)):

    mylog = models.GameLogSR(**gamelog.dict())
    
    db.add(mylog)
    db.commit()
    db.refresh(mylog)

    return mylog



