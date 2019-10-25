
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

    @staticmethod
    def get_service():
        qry = []
        with sql_cursor() as db:
            qry = db.query(ServicesMd.id, ServicesMd.label).all()
        
        return qry 


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

    @staticmethod
    def get_items(id):
        qry = ()
        with sql_cursor() as db:
            qry = db.query(ServiceItems.id, ServiceItems.name, 
                           ServiceItems.name, ServiceItems.label, 
                           ServiceItems.image, ServiceItems.service_id
                           ).filter_by(id=id).first()
        return qry 



class MobileUser(Base):

    __tablename__ = "registered_users"

    id = Column(BigInteger, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(30), nullable=False)

    # field to determine if a user is active or inactive 
    active = Column(Boolean)




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

    
