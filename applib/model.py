
from contextlib import contextmanager
from sqlalchemy import (create_engine, Integer, String,
                        Text, DateTime, BigInteger, Date, 
                        Column, ForeignKey, or_, Sequence, Boolean)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from applib.lib import helper as h 
import datetime 

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

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    label = Column(String(120),  nullable=False)
    image = Column(Text)
    category_name = Column(String(50), nullable=False)

    # field to determine of a service is active or inactive 
    active = Column(Boolean)

    @staticmethod
    def get_service():
        qry = ()
        with sql_cursor() as db:
            qry = db.query(ServicesMd.id, ServicesMd.label).all()
        
        return qry 


class ServiceItems(Base):
    
    __tablename__  = 'service_items'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    label = Column(String(100),  nullable=False)
    label_desc = Column(String(100), nullable=False)
    image = Column(Text)
    service_id = Column(BigInteger, ForeignKey("service_list.id"), 
                        nullable=False)

    # field to determine f a serviceItem is active or inactive 
    active = Column(Boolean)

    @staticmethod
    def get_items(id):
        qry = ()
        with sql_cursor() as db:
            qry = db.query(ServiceItems.id, ServiceItems.name, 
                           ServiceItems.name, ServiceItems.label, 
                           ServiceItems.image, ServiceItems.service_id,
                           ServiceItems.label_desc
                           ).filter_by(id=id).first()
        return qry 



class MobileUser(Base):

    __tablename__ = "registered_users"

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(30), nullable=False)
    mac_address = Column(String(15), nullable=False)

    # field to determine if a user is active or inactive 
    active = Column(Boolean)



class Transactions(Base):

    __tablename__ = "transactions_table"

    # remove the method with_variant 
    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, autoincrement=True)

    trans_ref = Column(String(100), nullable=False)    
    trans_desc = Column(String(100), nullable=False)
    trans_code = Column(String(30), nullable=False)
    trans_params = Column(Text, nullable=False)
    trans_resp = Column(Text, nullable=False)
    user_mac_address = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("registered_users.id"), nullable=False)
    trans_type_id = Column(Integer, ForeignKey("service_items.id"), nullable=False)
    date_created = Column(DateTime, nullable=False)

    
    @staticmethod
    def save(**kwargs):
        trans_ins = Transactions(**kwargs)
        trans_ins.date_created = datetime.datetime.now()

        with sql_cursor() as db:
            db.add(trans_ins)


    
    

def form2model(formobj, model_ins, exclude=[]):
    counter = 0            
    for key, obj in formobj._fields.items():
        if key in exclude:
            continue

        if hasattr(model_ins, key):
            setattr(model_ins, key, obj.data)
            counter += 1 

    assert counter > 0 , "No model instance fields not found."
     
def model2form(model_ins, form_ins, exclude=[]):

    counter = 0
    for key, obj in form_ins._fields.items():
        if key in exclude:
            continue
            
        if hasattr(model_ins, key):
            obj.data = getattr(model_ins, key)
            counter += 1

    assert counter > 0 , "No model instance fields not found."



def create_tbl():
    Base.metadata.create_all(ENGINE)
    


def drop_tbl():
    Base.metadata.drop_all(ENGINE)

    
