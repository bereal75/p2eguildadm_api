from decimal import Decimal
from turtle import back
from sqlalchemy import TIMESTAMP, BigInteger, Column, Integer, Numeric, String, Boolean, DateTime, null, Date
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

    alias = Column(String, nullable=False)
    walletaddress = Column(String, nullable=False)
    walletownerid = Column(BigInteger, ForeignKey("person.personid", ondelete="CASCADE"), nullable=False)
    walletid = Column(Integer, autoincrement=True, primary_key=True, nullable=False)

    # owner = relationship("person", back_populates="wallets")


class Deck(Base):
    __tablename__ = "deck"

    deckid = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    deckownerwalletid = Column(BigInteger, ForeignKey("wallet.walletid", ondelete="CASCADE"), nullable=False)
    deckscholarwalletid = Column(BigInteger, ForeignKey("wallet.walletid", ondelete="CASCADE"), nullable=False)
    scholarshareinpercent = Column(Numeric(precision=6, scale=2), nullable=False)
    payoutinstablecoinpercent = Column(Numeric(precision=6, scale=2), nullable=False)
    conversionratetostablecoin = Column(Numeric(precision=15, scale=6), nullable=False)
    payoutintervalindays = Column(Integer, default=7, nullable=False )
    validfrom = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()::DATE'))
    validuntil = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('\'2999-12-31\'::TIMESTAMPTZ'))


class WalletBalance(Base):
    __tablename__ = "walletbalance"

    walletbalanceid = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    walletid = Column(Integer, ForeignKey("wallet.walletid", ondelete="CASCADE"), nullable=False)
    crypto_tokenid = Column(Integer, ForeignKey("crypto_token.crypto_tokenid", ondelete="CASCADE"), nullable=False)
    balance = Column(Numeric(precision=36, scale=2), nullable=False)
    balance_dts = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()::DATE'))


class CryptoToken(Base):
    __tablename__ = "crypto_token"

    crypto_tokenid = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    tokentype = Column(String, nullable=True)
    tokenname = Column(String, nullable=True)
    contractaddress = Column(String, nullable=False)
    decimalpoints = Column(Integer, nullable=True )
    blockchain = Column(String, nullable=True)
    tracktotalsupply = Column(BigInteger, nullable=False, default=False)


class TokenSupply(Base):
    __tablename__ = "tokensupply"

    tokensupplyid = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    crypto_tokenid = Column(Integer, ForeignKey("crypto_token.crypto_tokenid", ondelete="CASCADE"), primary_key=True, nullable=False)
    tokensupply = Column(Numeric(precision=36, scale=2) ,nullable=False )
    tokensupply_dts = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()::DATE'))


class GameLogSR(Base):
    __tablename__ = "gamelogsr"

    gamelogsrid = Column(BigInteger, autoincrement=True, primary_key=True, nullable=False)
    log_dts = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()::DATE'))
    walletid = Column(BigInteger, ForeignKey("wallet.walletid", ondelete="CASCADE"), nullable=False)
    issnapshot = Column(Boolean, nullable=True, default=False)
    pending_earnings = Column(Integer, nullable=True)
    total_earnings = Column(BigInteger, nullable=True)
    current_energy = Column(Integer, nullable=True)
    max_energy = Column(Integer, nullable=True)
    changehash = Column(String, nullable=False)




# class GameLogSR(Base):
#     __tablename__ = "v_gamelogsr_extended"


#     log_dts = Column(TIMESTAMP(timezone=True))
#     log_date = Column(Date)
#     walletid = Column(BigInteger)
#     personid = Column(BigInteger)
#     alias = Column(String)
#     pending_earnings = Column(Integer)
#     total_earnings = Column(BigInteger)
#     current_energy = Column(Integer)
#     max_energy = Column(Integer)
#     RowNumLatestLog = Column(Integer)

