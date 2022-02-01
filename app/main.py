from genericpath import exists
from msilib import schema
from queue import Empty
from xmlrpc.client import boolean
from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.params import Body
from typing import List

from pydantic import BaseModel
import pydantic
from sqlalchemy import Boolean, true
from sqlalchemy.orm import Session
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings
from . import models, schemas
from .database import engine, get_db



print(f"This api is running on {settings.dcgdb_host}")

# binds sqlalchemy
models.Base.metadata.create_all(bind=engine)

# instantiate a fastapi class (our api)
app = FastAPI()


# retries = 0
# while retries <= 2:
#     try:
#         # TODO has to be put into environment variables
#         conn = psycopg2.connect(host=settings.dcgdb_host
#                                 , database = settings.dcgdb_dbname
#                                 , user = settings.dcgdb_user
#                                 , password = settings.dcgdb_pass
#                                 , cursor_factory=RealDictCursor )
#         cursor = conn.cursor()
#         print("Database connection established")
#         break

#     except Exception as error:
#         print("Database connection could not be established!")
#         print("Error: ", error)
#         retries = retries + 1
#         time.sleep(8 * retries)




# get all persons
@app.get("/persons", status_code=status.HTTP_200_OK, response_model=List[schemas.Person])
def get_persons(db: Session = Depends(get_db)):
    persons = db.query(models.Person).all()
    return persons  


# Get a specific person
@app.get("/persons/{personid}", status_code=status.HTTP_200_OK, response_model=schemas.Person)
def get_personsbytgchatid(personid: int, db: Session = Depends(get_db)):

    person = db.query(models.Person).filter(models.Person.personid == personid).first()

    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"person with telegramchatid <{personid}> was not found!")

    return person


# Create a person
@app.post("/persons", status_code=status.HTTP_201_CREATED, response_model=schemas.Person)
def post_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):

    new_person = models.Person(**person.dict())
    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return new_person


# insert a wallet
@app.post("/wallets", status_code=status.HTTP_201_CREATED, response_model=schemas.Wallet)
def post_wallet(wallet: schemas.WalletCreate, db: Session = Depends(get_db)):

    mywallet = models.Wallet(**wallet.dict())
    
    wallet_query = db.query(models.Wallet).filter(models.Wallet.walletaddress == mywallet.walletaddress).filter(models.Wallet.walletownerid == mywallet.walletownerid)

    if wallet_query.first() == None:
        db.add(mywallet)
        db.commit()
        db.refresh(mywallet)

        return wallet
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Wallet <{mywallet.walletaddress}> is already registered for owner <{mywallet.walletownerid}>. Wallet not inserted.")


#TODO update wallet alias
@app.put("/wallets/{walletaddress}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Wallet)
def update_wallet(walletaddress: str, updated_wallet : schemas.WalletUpdate, db: Session = Depends(get_db)):

    wallet_query = db.query(models.Wallet).filter(models.Wallet.walletaddress == walletaddress)

    wallettoupdate = wallet_query.first()

    if wallettoupdate == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"wallet <{walletaddress}> was not found!")
    else:
        wallet_query.update(updated_wallet.dict(), synchronize_session=False)
        db.commit()
        return wallet_query.first()


# get all wallets
@app.get("/wallets", status_code=status.HTTP_200_OK, response_model=List[schemas.Wallet])
def get_wallet(db: Session = Depends(get_db)):
    
    wallets = db.query(models.Wallet).all()
    return wallets


# get all wallets 
@app.get("/walletsbyperson/{personid}", status_code=status.HTTP_200_OK, response_model=List[schemas.Wallet])
def get_walletbyperson(personid: int, db: Session = Depends(get_db)):
    wallet_query = db.query(models.Wallet).filter(models.Wallet.walletownerid == personid)

    if wallet_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no wallets found.")
    else:
        wallets = wallet_query.all()
        #TODO convert to pydantic schema without walletid
        return wallets

    
   


# Delete a person
@app.delete("/persons/{personid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(personid: int, db: Session = Depends(get_db)):

    person = db.query(models.Person).filter(models.Person.personid == personid)
    
    if person.first() == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="person with id: {0} does not exist".format(personid))

    person.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a person (isadmin cannot be updated via API)
@app.put("/persons/{personid}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Person)
def update_person(personid: int, updated_person: schemas.PersonUpdate, db: Session = Depends(get_db)):
    
    person_query = db.query(models.Person).filter(models.Person.personid == personid)

    persontoupdate = person_query.first()

    if persontoupdate == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"person <{personid}> was not found!")    

    person_query.update(updated_person.dict(), synchronize_session=False)
    db.commit()

    return person_query.first()






    


