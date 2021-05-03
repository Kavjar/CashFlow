import os
import sys

from sqlalchemy import (INTEGER, DATE, VARCHAR, Column, ForeignKey)
from sqlalchemy.orm import relationship

sys.path.append(os.getcwd())
from restful_api import Base, engine


class Account(Base):
    __tablename__ = "account"
    id_account = Column(INTEGER, primary_key=True)
    sum = Column(INTEGER, nullable=True)


class Finances(Base):
    __tablename__ = "finances"
    id_fin = Column(INTEGER, primary_key=True)
    item = Column(VARCHAR(45))
    price = Column(INTEGER)
    date = Column(DATE)
    account_id = Column(INTEGER, ForeignKey(Account.id_account))
    Account = relationship(Account)
    status = Column(VARCHAR(45))

    def get_finances(self):
        result = {
            'id': self.id_fin,
            'item': self.item,
            'price': self.price,
            'date': self.date,
            'status': self.status
        }
        return result


class Family(Base):
    __tablename__ = "family"

    id_family = Column(INTEGER, primary_key=True)
    surname = Column(VARCHAR(45), nullable=True)
    budget = Column(INTEGER)


class User(Base):
    __tablename__ = "user"

    id_user = Column(INTEGER, primary_key=True)
    username = Column(VARCHAR(45), nullable=True)
    firstname = Column(VARCHAR(45))
    lastname = Column(VARCHAR(45))
    email = Column(VARCHAR(45))
    password = Column(VARCHAR(45), nullable=True)
    phone = Column(VARCHAR(45))
    account_id = Column(INTEGER, ForeignKey(Account.id_account))
    Account = relationship(Account)
    family_id = Column(INTEGER, ForeignKey(Family.id_family), nullable=True)
    Family = relationship(Family)

    def get_users(self):
        result = {
            'id': self.id_user,
            'username': self.username,
            'password': self.password,
            'family id': self.family_id,
            'account id': self.account_id
        }
        return result

    def get_users2(self):
        result = {
            'id': self.id_user,
            'username': self.username,
            'family id': self.family_id,
            'account id': self.account_id
        }
        return result


class Transaction(Base):
    __tablename__ = "transactiondata"

    id_transaction = Column(INTEGER, primary_key=True)
    money = Column(INTEGER, nullable=True)
    direction = Column(INTEGER, nullable=True)
    family_id = Column(INTEGER, ForeignKey(Family.id_family))
    Family = relationship(Family)
    account_id = Column(INTEGER, ForeignKey(Account.id_account))
    Account = relationship(Account)

    def get_transaction(self):
        result = {
            'id': self.id_transaction,
            'money': self.money,
            'direction': self.direction,
            'family id': self.family_id,
            'account id': self.account_id
        }
        return result


Base.metadata.create_all(engine)
