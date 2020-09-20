from sqlalchemy import Column, Integer, String, Binary, Date, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from contextlib import contextmanager


engine = create_engine('sqlite:///master_stats.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    main_race = Column(Integer)
    matchups = Column(Binary)


class BWMap(Base):
    __tablename__ = 'bwmap'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Tournament(Base):
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    # Map and tournament
    bwmap_id = Column(Integer, ForeignKey('bwmap.id'))
    bwmap = relationship('BWMap', foreign_keys=[bwmap_id])
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship('Tournament', foreign_keys=[tournament_id])
    # Players' info
    winner_id = Column(Integer, ForeignKey('player.id'))
    winner = relationship('Player', foreign_keys=[winner_id])
    loser_id = Column(Integer, ForeignKey('player.id'))
    loser = relationship('Player', foreign_keys=[loser_id])
    winner_race = Column(Integer, nullable=False)
    loser_race = Column(Integer, nullable=False)


@contextmanager
def session_manager():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


Base.metadata.create_all(engine)
