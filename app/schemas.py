from sqlite3 import Timestamp
import string
from typing import List, Optional
from unicodedata import decimal
from xmlrpc.client import boolean

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

from sqlalchemy import TIMESTAMP, Boolean, Integer



#### PERSON

# this class is used for the response of the api
class Person(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    tgusername: Optional[str]

    class Config:
        orm_mode = True

class PersonBase(BaseModel):
    personid: int
    firstname: Optional[str]
    lastname: Optional[str]
    tgusername: Optional[str]
    createdate: Optional[datetime]   


class PersonCreate(PersonBase):
    pass
    class Config:
        orm_mode = True

class PersonUpdate(PersonBase):
    firstname: Optional[str]
    lastname: Optional[str]
    tgusername: Optional[str]
    class Config:
        orm_mode = True



#### WALLET
# class Wallet(BaseModel):
#     alias: str
#     walletaddress: str

#     class Config:
#         orm_mode = True

class WalletBase(BaseModel):
    walletid: Optional[int]
    alias: str
    walletaddress: str
    walletownerid: int
    class Config:
        orm_mode = True

class WalletCreate(WalletBase):
    alias: str
    walletaddress: str
    walletownerid: int

    class Config:
        orm_mode = True

class WalletUpdate(WalletBase):
    pass

    class Config:
        orm_mode = True

class DeckBase(BaseModel):
    deckid: Optional[int]


    class Config:
        orm_mode = True

class Deck(DeckBase):
    deckownerwalletid: int
    deckscholarwalletid: int
    scholarshareinpercent: Decimal
    payoutinstablecoinpercent: Decimal
    conversionratetostablecoin: Decimal
    payoutintervalindays: Optional[int]
    validfrom: Optional[datetime]
    validuntil: Optional[datetime]


    class Config:
        orm_mode = True


class DeckCreate(DeckBase):
    deckownerwalletid: int
    deckscholarwalletid: int
    scholarshareinpercent: Decimal
    payoutinstablecoinpercent: Decimal
    conversionratetostablecoin: Decimal


    class Config:
        orm_mode = True


class DeckClose(DeckBase):
    deckownerwalletid: int
    validuntil: datetime


class WalletBalanceBase(BaseModel):
    walletbalanceid: Optional[int]
    walletid: int
    crypto_tokenid: int
    balance: Decimal
    balance_dts: Optional[datetime]

    class Config:
        orm_mode = True


class WalletBalanceCreate(WalletBalanceBase):
    pass

    class Config:
        orm_mode = True

class CryptoTokenBase(BaseModel):
    crypto_tokenid: int
    tokentype: Optional[str]
    tokenname: Optional[str]
    contractaddress : str
    decimalpoints : int
    blockchain : Optional[str]

    class Config:
        orm_mode = True


class TokenSupplyBase(BaseModel):
    crypto_tokenid : int
    tokensupply : Decimal
    tokensupply_dts : Optional[datetime]
    class Config:
        orm_mode = True


class GameLogSRBase(BaseModel):

    gamelogsrid : Optional[int]
    log_dts : Optional[datetime]
    walletid : int
    issnapshot : Optional[bool]
    pending_earnings : Optional[int]
    total_earnings : Optional[int]
    current_energy : Optional[int]
    max_energy : Optional[int]
    changehash : str

    class Config:
        orm_mode = True


class GameLogSRShort(BaseModel):
    pending_earnings : Optional[int]
    total_earnings : Optional[int]
    current_energy : Optional[int]
    max_energy : Optional[int]

    class Config:
        orm_mode = True


class RecruitmentBase(BaseModel):
    recruitmentid : int
    walletid : int
    walletaddress : str
    recruitingsamurais : Optional[str]
    blockno : int
    missioncomplete : bool
    missionduration : int

    class Config:
        orm_mode = True


class RecruitmentId(BaseModel):
    recruitmentid : int

    class Config:
        orm_mode = True