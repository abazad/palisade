from sqlalchemy import Column, Integer, String, Sequence, Date, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SQ_User(Base):
    __tablename__ = 'sq_user'
    
    id = Column(Integer, Sequence('sq_user_id_seq'), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    login = Column(String(50), unique=True)
    password = Column(String(250))
    email = Column(String(250), unique=True)
    is_admin = Column(Boolean())
    status = Column(String(3))
    traffic_limit = Column(Integer(9))
    
    def __init__(self, first_name, last_name, login, password, email, is_admin, status, traffic_limit):
        self.first_name = first_name
        self.last_name = last_name
        self.login = login
        self.password = password
        self.email = email
        self.is_admin = is_admin
        self.status = status
        self.traffic_limit = traffic_limit
    
    def __repr__(self):
        return "<SQ_USER('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % \
            (self.first_name, self.last_name, self.login, 'secret',\
             self.email, self.is_admin, self.status, self.traffic_limit)


class SQ_Access_Log_Data(Base):
    __tablename__ = 'sq_access_log_data'
    
    id = Column(Integer, Sequence('sq_access_log_data_sq'), primary_key=True)
    access_time = Column(Date)
    response_time = Column(Integer)
    client_src_ip = Column(String(15))
    sq_req_status = Column(String(64))       
    http_status_code = Column(String(4))
    bytes = Column(Integer(9))
    req_method = Column(String(10))
    user_name = Column(String(32))
    sq_hierarchy_status = Column(String(32))
    server_fqdn = Column(String(255))
    mime_type = Column(String(32))
    mime_type_desc = Column(String(32))
    url = Column(String(4000))
    url_hostname = Column(String(255))
    
    def __init__(self, access_time, response_time, client_src_ip, sq_req_status,
                 http_status_code, bytes, req_method, user_name, 
                 sq_hierarchy_status, server_ip, mime_type, mime_type_desc,url,
                 url_hostname):  
        self.access_time = access_time
        self.response_time = response_time
        self.client_src_ip = client_src_ip
        self.sq_req_status = sq_req_status
        self.http_status_code = http_status_code
        self.bytes = bytes
        self.req_method = req_method
        self.user_name = user_name
        self.sq_hierarchy_status = sq_hierarchy_status
        self.server_ip = server_ip
        self.mime_type = mime_type
        self.mime_type_desc = mime_type_desc
        self.url = url
        self.url_hostname = url_hostname

    def __repr__(self):
        return "<SQ_ACCESS_LOG_DATA(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s>" % \
        (self.access_time, self.response_time, self.client_src_ip, 
         self.sq_req_status, self.http_status_code, self.bytes, 
         self.req_method, self.user_name, self.sq_hierarchy_status, 
         self.server_ip, self.mime_type, self.mime_type_desc, 
         self.url, self.url_hostname)

class SQ_Lost_Password(Base):
    __tablename__='SQ_LOST_PASSWORD'
    id = Column(Integer(9), Sequence('sq_lost_password_seq'), primary_key=True)
    created_on = Column(Date)
    email = Column(String(250))
    state = Column(String(50))
    secret_key = Column(String(32))
    
    def __init__(self, created_on, email, state, secret_key):
        self.created_on = created_on
        self.email = email
        self.state = state
        self.secret_key = secret_key
    
    def __repr__(self):
        return "<SQ_LOST_PASSWORD('%s', '%s', '%s', '%s')>" %\
             (self.created_on, self.email, self.state, self.secret_key)

class SQ_Report_Data(Base):
    __tablename__ = 'SQ_REPORT_DATA'
    id = Column(Integer(9), Sequence('sq_report_data_seq'), primary_key=True)
    created_on = Column(Date)
    report_name = Column(String(150))
    data = Column(Text(6000))
    
    def __init__(self, created_on, report_name, data):
        self.created_on = created_on
        self.report_name = report_name
        self.data = data
    
    def __repr__(self):
        return "<SQ_REPORT_DATA('%s', '%s')>" % (self.created_on, self.report_name)
        
