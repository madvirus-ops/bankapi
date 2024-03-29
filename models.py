from database import Base
from sqlalchemy import Column,String,Integer,ForeignKey,Boolean,Float,DateTime
from sqlalchemy.sql import func
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
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String,unique=True)
    phoneNumber = Column(String)
    password = Column(String)
    profile_image = Column(String,default='/media/profile_image/image.png')
    email_verified = Column(Boolean,default = False)
    balance = Column(String,default="10")
    dollar_balance = Column(String,default="10")


    pin = relationship("UserPin",back_populates="user",cascade="all, delete-orphan")
    re_balance  = relationship("UserAccountBalance",back_populates="user",cascade="all, delete-orphan")
    blogs = relationship("BlogModel",back_populates="owner",cascade="all, delete-orphan")
    accounts = relationship("UserReservedAccount", back_populates = "user",cascade="all, delete-orphan")
    data_subscriptions = relationship("UserDataTransactions", back_populates = "user",cascade="all, delete-orphan")
    mapple_id = relationship("MappleradCustomer", back_populates="user",cascade="all, delete-orphan")
    dollar_card = relationship("VirtualCards", back_populates="user",cascade="all, delete-orphan")



class AdminModel(Base):
    __tablename__ = 'admin'

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String,unique=True)
    phoneNumber = Column(String)
    password = Column(String)
    email_verified = Column(Boolean,default = False)
    vtu_balance = Column(Integer,default = 10)



class UserPin(Base):
    __tablename__ = "userpin"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('Users.id'))
    pin = Column(Integer)
    user = relationship("UserModel",back_populates= "pin")




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
    accountReference = Column(String)


class UserReservedAccount(Base):
    __tablename__ = "user_accounts"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('Users.id'))
    bank_code = Column(String)
    bank_name = Column(String)
    AccountNumber = Column(String)
    AccountName = Column(String)
    user = relationship("UserModel",back_populates= "accounts")


class UserAccountBalance(Base):
    __tablename__ = "account_balance"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('Users.id'))
    amount = Column(Integer, default = 0)
    user = relationship("UserModel",back_populates= "re_balance")



class UserDataTransactions(Base):
    __tablename__ = 'data_transactions'
    
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('Users.id'))
    network = Column(Integer)
    payment_medium = Column(String)
    mobile_number = Column(String)
    plan = Column(Integer)
    status = Column(String)
    plan_network = Column(String)
    plan_name = Column(String)
    plan_amount = Column(Float)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("UserModel",back_populates= "data_subscriptions")



class CyberDataPlans(Base):
    __tablename__ = "data_plans"
    id = Column(Integer,primary_key=True,index=True)
    plan_id = Column(Integer)
    plan_price = Column(Float)
    network = Column(String)
    size = Column(String)
    validity = Column(String)

class CyberNetwork(Base):
    __tablename__ = "network"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    network_id = Column(Integer)



class MappleradCustomer(Base):
    __tablename__ = "mapple_customers"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('Users.id'))
    customer_id = Column(String)
    user = relationship("UserModel",back_populates= "mapple_id")

    


class VirtualCards(Base):
    __tablename__ = "virtual_cards"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('Users.id'))
    card_id = Column(String,default="")
    customer_id = Column(String,default="")
    card_name = Column(String,default="")
    card_number = Column(String,default="")
    masked_pan = Column(String,default="")
    expiry = Column(String,default="")
    cvv = Column(String,default="")
    status = Column(String,default="")
    card_type = Column(String,default="")
    issuer = Column(String,default="")
    currency = Column(String,default="")
    balance = Column(String,default="")
    street = Column(String,default="")
    city = Column(String,default="")
    state = Column(String,default="")
    postal_code = Column(String,default="")
    country = Column(String,default="")
    created_at = Column(String,default="")
    updated_at = Column(String,default="")
    reference = Column(String,default="")
    user = relationship("UserModel",back_populates= "dollar_card")



