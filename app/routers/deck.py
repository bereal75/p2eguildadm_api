from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import Boolean, desc, true
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas, utils

router = APIRouter()


# get all decks
@router.get("/decks", status_code=status.HTTP_200_OK,response_model=List[schemas.Deck])
def get_decks(db: Session = Depends(get_db)):

    decks = db.query(models.Deck).all()
    return decks



# update an existing deck (close deck)
@router.put("/decks/closedeck/{deckid}",status_code=status.HTTP_202_ACCEPTED, response_model=List[schemas.DeckClose])
def close_deck(deckid: int, closed_deck: schemas.DeckClose, db: Session = Depends(get_db)):


    deck_query = db.query(models.Deck).filter(models.Deck.deckid == deckid).filter(models.Deck.deckownerwalletid == closed_deck.deckownerwalletid)

    decktoupdate = deck_query.first()

    if decktoupdate == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Deck <{deckid}> was not found!")
    else:
        deck_query.update(closed_deck.dict(), synchronize_session=False)
        db.commit()
        return deck_query.first()

# # get current deck of deck owner wallet id
# @router.get("/decks/{deckownerwalletid}", status_code=status.HTTP_200_OK,response_model=List[schemas.Deck])
# def get_current_deck(deckownerwalletid: int, db: Session = Depends(get_db)):




# insert a wallet
@router.post("/decks", status_code=status.HTTP_201_CREATED, response_model=schemas.Deck)
def post_wallet(deck: schemas.DeckCreate, db: Session = Depends(get_db)):

    mydeck = models.Deck(**deck.dict())
    
    deck_query = db.query(models.Deck).filter(models.Deck.deckownerwalletid == mydeck.deckownerwalletid).filter(models.Deck.validuntil == '2999-12-31 00:00:00.000 +0000')

    if deck_query.first() == None:
        db.add(mydeck)
        db.commit()
        db.refresh(mydeck)

        return deck
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Deck <{mydeck.deckownerwalletid}> is already registered. Deck not inserted. Close the deck in question first.")