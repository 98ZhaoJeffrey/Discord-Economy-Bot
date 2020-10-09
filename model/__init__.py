from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship 

engine = create_engine(database key goes here)
Base = declarative_base()
def to_dict(self):
    return {c.name:getattr(self, c.name, None) for c in self.__table__.columns}
Base.to_dict = to_dict

class User(Base):
    __tablename__ = 'user'
    username = Column('username', String(37), nullable = False, primary_key = True)
    balance = Column('balance', Integer, nullable = False, default = 0)
    last_dropdate = Column('dropdate', DateTime, nullable=True)
    items = relationship("Item", back_populates="user")
    
class Item(Base):
    __tablename__ = 'item'
    iid = Column('iid', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(50), nullable = False)
    quantity = Column('quantity', Integer, nullable = False)
    price = Column('price', Integer, nullable = False)
    owner = Column(String(37), ForeignKey('user.username'))
    user = relationship("User", back_populates="items")

#Base.metadata.drop_all(engine)
#Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)