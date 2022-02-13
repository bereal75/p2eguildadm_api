from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
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
from .routers import person, gamelogsr, recruitment, wallet, deck, tokensupply



print(f"This api is running on {settings.p2eguildadm_host}")

# binds sqlalchemy
models.Base.metadata.create_all(bind=engine)

# instantiate a fastapi class (our api)
app = FastAPI()


origins = {"http://localhost:7999"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(person.router)
app.include_router(gamelogsr.router)
app.include_router(wallet.router)
app.include_router(deck.router)
app.include_router(tokensupply.router)
app.include_router(recruitment.router)

@app.get("/")
def root():
    return {"message" : "This is the p2eguildadmin API. Open your browser and open /docs to see the documentation for this API." }









    

