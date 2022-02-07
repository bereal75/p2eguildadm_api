from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from fastapi.params import Body
from typing import List

from pydantic import BaseModel
import pydantic
from sqlalchemy import Boolean, desc, true
from sqlalchemy.orm import Session
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings
from . import models, schemas
from .database import engine, get_db
from .routers import person, gamelogsr, wallet, deck



print(f"This api is running on {settings.p2eguildadm_host}")

# binds sqlalchemy
models.Base.metadata.create_all(bind=engine)





# instantiate a fastapi class (our api)
app = FastAPI()


app.include_router(person.router)
app.include_router(gamelogsr.router)
app.include_router(wallet.router)
app.include_router(deck.router)

@app.get("/")
def root():
    return {"message" : "This is the p2eguildadmin API. Open your browser and open /docs to see the documentation for this API." }





@app.get("/cryptotokens", status_code=status.HTTP_200_OK,response_model=List[schemas.CryptoTokenBase])
def get_cyptotokens(db: Session = Depends(get_db)):

    tokens = db.query(models.CryptoToken).all()
    return tokens

@app.get("/cryptotokens/tracktotalsupply", status_code=status.HTTP_200_OK,response_model=List[schemas.CryptoTokenBase])
def get_cyptotokens(db: Session = Depends(get_db)):

    tokens = db.query(models.CryptoToken).filter(models.CryptoToken.tracktotalsupply == True).all()
    return tokens


@app.post("/walletbalance", status_code=status.HTTP_201_CREATED, response_model=schemas.WalletBalanceCreate)
def post_walletbalance(walletbalance: schemas.WalletBalanceBase, db: Session = Depends(get_db)):

    mywalletbalance = models.WalletBalance(**walletbalance.dict())
    
    db.add(mywalletbalance)
    db.commit()
    db.refresh(mywalletbalance)

    return walletbalance


@app.post("/tokensupply", status_code=status.HTTP_201_CREATED, response_model=schemas.TokenSupplyBase)
def post_walletbalance(tokensupply: schemas.TokenSupplyBase, db: Session = Depends(get_db)):

    mysupply = models.TokenSupply(**tokensupply.dict())
    
    db.add(mysupply)
    db.commit()
    db.refresh(mysupply)

    return mysupply





    


