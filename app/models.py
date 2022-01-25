from sqlalchemy import BigInteger, Column, Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Person(Base):
    __tablename__ = "person"
    personid = Column(BigInteger, primary_key=True, nullable=False)
    firstname = Column(String,nullable=True)
    lastname = Column(String,nullable=True)
    tgusername = Column(String,nullable=True)
    isadmin = Column(Boolean,server_default='FALSE')
    #createdate = Column(DateTime,server_default='2022-01-14 00:00')
    #TODO timestamp conversion 

    walletowner = relationship("wallet", back_populates="walletowner")


class Wallet(Base):
    __tablename__ = "wallet"
    walletid = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    walletaddress = Column(String, nullable=False)
    walletownerid = Column(BigInteger, ForeignKey("person.personid"), nullable=False)

    walletowner = relationship("person", back_populates="wallet")

