from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SQ_User(Base):
    __tablename__ = 'sq_user'
    
    id = Column(Integer, Sequence('sq_user_id_seq'), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    password = Column(String(250))
    status = Column(String(3))
    traffic_limit = Column(Integer(9))
    
    def __init__(self, first_name, last_name, password, status, traffic_limit):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.status = status
        self.traffic_limit = traffic_limit
    
    def __repr__(self):
        return "<SQ_USER('%s', '%s', '%s', '%s', '%s')>" % (self.first_name, self.last_name, 'secret', self.status, self.traffic_limit)


