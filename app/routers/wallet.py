from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import Boolean, desc, true
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas, utils

router = APIRouter()


# insert a wallet
@router.post("/wallets", status_code=status.HTTP_201_CREATED, response_model=schemas.WalletBase)
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
@router.put("/wallets/{walletaddress}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.WalletBase)
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
@router.get("/wallets", status_code=status.HTTP_200_OK, response_model=List[schemas.WalletBase])
def get_wallet(db: Session = Depends(get_db)):
    
    wallets = db.query(models.Wallet).all()
    return wallets


# get all wallets 
@router.get("/walletsbyperson/{personid}", status_code=status.HTTP_200_OK, response_model=List[schemas.WalletBase])
def get_walletbyperson(personid: int, db: Session = Depends(get_db)):
    wallet_query = db.query(models.Wallet).filter(models.Wallet.walletownerid == personid)

    if wallet_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no wallets found.")
    else:
        wallets = wallet_query.all()
        #TODO convert to pydantic schema without walletid
        return wallets

@router.post("/walletbalance", status_code=status.HTTP_201_CREATED, response_model=schemas.WalletBalanceCreate)
def post_walletbalance(walletbalance: schemas.WalletBalanceBase, db: Session = Depends(get_db)):

    mywalletbalance = models.WalletBalance(**walletbalance.dict())
    
    db.add(mywalletbalance)
    db.commit()
    db.refresh(mywalletbalance)

    return walletbalance
