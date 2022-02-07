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
from .routers import person, gamelogsr, wallet, deck, cryptotokens



print(f"This api is running on {settings.p2eguildadm_host}")

# binds sqlalchemy
models.Base.metadata.create_all(bind=engine)

# instantiate a fastapi class (our api)
app = FastAPI()


app.include_router(person.router)
app.include_router(gamelogsr.router)
app.include_router(wallet.router)
app.include_router(deck.router)
app.include_router(cryptotokens.router)

@app.get("/")
def root():
    return {"message" : "This is the p2eguildadmin API. Open your browser and open /docs to see the documentation for this API." }









    


