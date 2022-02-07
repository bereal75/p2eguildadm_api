from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import Boolean, desc, true
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas, utils


router = APIRouter()

@router.get("/cryptotokens", status_code=status.HTTP_200_OK,response_model=List[schemas.CryptoTokenBase])
def get_cyptotokens(db: Session = Depends(get_db)):

    tokens = db.query(models.CryptoToken).all()
    return tokens

@router.get("/cryptotokens/tracktotalsupply", status_code=status.HTTP_200_OK,response_model=List[schemas.CryptoTokenBase])
def get_cyptotokens(db: Session = Depends(get_db)):

    tokens = db.query(models.CryptoToken).filter(models.CryptoToken.tracktotalsupply == True).all()
    return tokens

@router.post("/tokensupply", status_code=status.HTTP_201_CREATED, response_model=schemas.TokenSupplyBase)
def post_walletbalance(tokensupply: schemas.TokenSupplyBase, db: Session = Depends(get_db)):

    mysupply = models.TokenSupply(**tokensupply.dict())
    
    db.add(mysupply)
    db.commit()
    db.refresh(mysupply)

    return mysupply


