from database import Base
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship



class BlogModel(Base):
    __tablename__ = 'Blog'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer,ForeignKey('Users.id'))
    owner = relationship("UserModel",back_populates="blogs")


class UserModel(Base):
    __tablename__ = 'Users'

    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String,unique=True)
    phoneNumber = Column(String)
    password = Column(String) 

    blogs = relationship("BlogModel",back_populates="owner")


class Banks(Base):
    __tablename__ = 'banks'
    id = Column(Integer,primary_key=True,index=True)
    bank_id = Column(Integer)
    code = Column(String)
    name = Column(String)


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('Users.id'))
    customer_id = Column(String)


class AccountRef(Base):
    __tablename__ = 'account_ref'
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('Users.id'))
    reference = Column(String)





