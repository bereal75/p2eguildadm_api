from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime



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
class Wallet(BaseModel):
    alias: str
    walletaddress: str

    class Config:
        orm_mode = True

class WalletBase(BaseModel):
    alias: str
    walletaddress: str
    walletownerid: int

class WalletCreate(WalletBase):
    alias: Optional[str]
    walletaddress: str
    walletownerid: int

    class Config:
        orm_mode = True

class WalletUpdate(WalletBase):
    pass

    class Config:
        orm_mode = True