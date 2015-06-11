from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class PlayList(Base):
    __tablename__ = 'playList'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    author = Column(String(30))
    tags = Column(String(50))
    description = Column(String(200))
    playNum = Column(Integer)
    listLen = Column(Integer)


class music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    lyric = Column(String(1000))

url = 'mysql+mysqlconnector://root:@localhost:3306/test'
engine = create_engine(url)

DBSession = sessionmaker(bind=engine)
session = DBSession()
session.add(music(name="test", lyric="test"))
session.commit()
session.close()
