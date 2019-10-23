
from contextlib import contextmanager

from sqlalchemy import (create_engine, Integer, String,
                        Text, DateTime, BigInteger, Date, 
                        Column, ForeignKey, or_, Sequence, Boolean)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from applib.lib import helper as h 

Base = declarative_base()
ENGINE = create_engine(h.set_db_uri(), echo=True)



@contextmanager  
def sql_cursor():
    
    Session = sessionmaker(bind=ENGINE)
    session = Session()

    try:         
        yield session
        session.commit()
    except Exception as e:  
        session.rollback()    
        raise e 

    finally:
        session.close()



class ServicesMd(Base):
    __tablename__  = 'service_list'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    label = Column(String(120),  nullable=False)
    image = Column(Text)
    category_name = Column(String(50), nullable=False)

    # field to determine of a service is active or inactive 
    active = Column(Boolean)


class ServiceItems(Base):
    
    __tablename__  = 'service_items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    label = Column(String(120),  nullable=False)
    image = Column(Text)
    service_id = Column(Integer, ForeignKey("service_list.id"), 
                        nullable=False)

    # field to determine f a serviceItem is active or inactive 
    active = Column(Boolean)


class MobileUser(Base):

    __tablename__ = "registered_users"

    id = Column(BigInteger, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(30), nullable=False)

    # field to determine if a user is active or inactive 
    active = Column(Boolean)



# class Users(Base):
#     __tablename__ = 'users'

#     id = Column(BigInteger, primary_key=True)    
#     username = Column(String(150), nullable=True)
#     password = Column(String(150), nullable=True)     



def create_tbl():
    Base.metadata.create_all(ENGINE)
    


def drop_tbl():
    Base.metadata.drop_all(ENGINE)

    
