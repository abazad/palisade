'''
Created on Jul 14, 2013

@author: bova
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("oracle://hr:Q1w3tre321@fbs", echo=True)
Session = sessionmaker(engine)


if __name__ == '__main__':
    print engine
    engine.execute("select 1 from dual").scalar()
    session = Session()
    print session