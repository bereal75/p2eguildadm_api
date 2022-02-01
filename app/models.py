from turtle import back
from sqlalchemy import TIMESTAMP, BigInteger, Column, Integer, String, Boolean, DateTime, null
from sqlalchemy import ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base

class Person(Base):
    __tablename__ = "person"

    personid = Column(BigInteger, primary_key=True, nullable=False)
    firstname = Column(String,nullable=True)
    lastname = Column(String,nullable=True)
    tgusername = Column(String,nullable=True)
    createdate = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # wallets = relationship("wallet", back_populates="owner")




class Wallet(Base):
    __tablename__ = "wallet"

    alias = Column(String, nullable=True)
    walletaddress = Column(String, nullable=False)
    walletownerid = Column(BigInteger, ForeignKey("person.personid", ondelete="CASCADE"), nullable=False)
    walletid = Column(Integer, autoincrement=True, primary_key=True, nullable=False)

    # owner = relationship("person", back_populates="wallets")


