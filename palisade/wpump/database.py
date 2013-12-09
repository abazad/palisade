'''
Created on 15.03.2013

@author: bova
'''
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from structure import download_state

DATABASE_FILE='c:/tmp/wpump.db'
db = create_engine('sqlite:///c:/tmp/wpump.db')
Base = declarative_base()
Session = sessionmaker(bind=db)
session = Session()

class WpumpTask(Base):
    __tablename__ = 'wpump_task'
    __table_args__ = {'sqlite_autoincrement': True}
    
    id = Column(Integer, primary_key=True)
    url = Column(String)
    size = Column(Integer)
    state = Column(String)
    created_on = Column(DateTime)    
    email = Column(String)
    size_completed = Column(Integer)
    
    def __init__(self, url, email, state=download_state['new']):
        self.url = url
        self.email = email
        self.state = state
    
    def __repr__(self):
        return "<WpumpTask('%s', '%s', '%s', %s)>" % (self.id, self.url, self.email, self.state)


class DBConnection(object):
    def __init__(self):
        super(DBConnection, self).__init__()
        self.conn = sqlite3.connect(DATABASE_FILE, check_same_thread = False)
        self.cursor = self.conn.cursor()
    
    def init_db(self):
        self.cursor.execute('''create table wpump_task(url text, state text)''')
        self.conn.commit()


def init_db():
    Base.metadata.create_all(db)

def drop_db():
    Base.metadata.drop_all(db)

def recreate_db():
    drop_db()
    init_db()
        
if __name__ == '__main__':
    db_conn = DBConnection()
    db_conn.init_db()


