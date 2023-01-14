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
    name = Column(String)
    email = Column(String,unique=True)
    password = Column(String) 

    blogs = relationship("BlogModel",back_populates="owner")


class Banks(Base):
    __tablename__ = 'banks'
    id = Column(Integer,primary_key=True,index=True)
    bank_id = Column(Integer)
    code = Column(String)
    name = Column(String)



