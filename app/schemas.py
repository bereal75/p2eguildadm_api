from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime

from typing import List, Optional


class Person(BaseModel):
    personid: int
    firstname: Optional[str]
    lastname: Optional[str]
    tgusername: Optional[str]
    createdate: Optional[datetime]

    class Config:
        orm_mode = True



class Wallet(BaseModel):
    walletid: int
    walletaddress: str
    walletownerid: int

    class Config:
        orm_mode = True