# -*- coding: utf-8 -*-
import MySQLdb  # noqa
from sqlalchemy import (create_engine, Column, Integer, String,
                        Boolean, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from cred import getDB, setEnv, getEnv

"""
Cred.py is not stored in the repo, it returns a string that has the server info
Ex: "mysql+mysqldb://" + USER + ":" + PASS + "@" + HOST + ":" + PORT + "/" + DB
"""

engine = create_engine(getDB('dev'))
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Stream(Base):
    __tablename__ = 'streams'

    id = Column(Integer, primary_key=True)
    game = Column(String(256), nullable=False)
    display_game = Column(String(256), nullable=False)
    url = Column(String(256), nullable=False)
    preview_location = Column(String(256), nullable=False)
    channel_name = Column(String(256), nullable=False)
    viewers = Column(String(256), nullable=False)
    status = Column(String(256), nullable=False)

    def __repr__(self):
        return "<Stream(game='%s', display_game='%s', url='%s', \
                preview_location='%s', channel_name='%s', \
                viewers='%s, status ='%s')>" % (self.game,
                                                self.display_game,
                                                self.url,
                                                self.preview_location,
                                                self.channel_name,
                                                self.viewers, self.status)


class Info(Base):
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True)
    starting_load = Column(Boolean, nullable=False)
    last_updated = Column(DateTime, nullable=False)
    donation_total = Column(Integer)
    maintenance_mode = Column(Boolean)

    def __repr__(self):
        return "<Info(starting_load='%s', last_updated='%s'>" % (
            self.starting_load, self.last_updated)


def multiStreamInsert(list_of_dicts):
    session = Session()
    deleteAllStreams(session)

    # Insert multiple streams into the DB
    if list_of_dicts:
        session.add_all(list_of_dicts)

    # Commit then close session
    session.commit()
    session.close()


def createSchema():
    # If DB schema doesn't exist, create it.
    Base.metadata.create_all(engine)


def getStreams():
    session = Session()

    if checkLoading() is False:
        dict_to_return = {}
        # Create a list full of dictionaries that have the twitch channel info.
        for instance in session.query(Stream):
            try:
                dict_to_return[instance.game].append(
                    {'stream_category': instance.game,
                     'display_name': instance.display_game,
                     'url': instance.url,
                     'viewers': instance.viewers,
                     'preview_location': instance.preview_location,
                     'channel_name': instance.channel_name,
                     'status': instance.status
                     }
                    )
            except:
                # If the list of dictionaries doesn't exist yet, create it.
                dict_to_return[instance.game] = [
                    {'stream_category': instance.game,
                     'display_name': instance.display_game,
                     'url': instance.url,
                     'viewers': instance.viewers,
                     'preview_location': instance.preview_location,
                     'channel_name': instance.channel_name,
                     'status': instance.status
                     }]

        last_query = session.query(Info).filter(Info.id == 1)
        last_updated = last_query.first().last_updated
        diff = datetime.now() - last_updated
        session.close()

        return ([dict_to_return, diff.seconds/60])
    else:
        session.close()
        return True


# Doesn't close session (Intentional)
def deleteAllStreams(session):
    for instance in session.query(Stream):
        session.delete(instance)
    session.commit()


def setLoading(setBool):
    session = Session()
    # Check to see id(1) exists - table should only ever have one row.
    try:
        server_info_query = session.query(Info).filter(Info.id == 1)
        result = server_info_query.first()
        result.starting_load = setBool
        if setBool is False:
            result.last_updated = datetime.now()
        session.commit()

    except:
        # If it doesn't exist create it with the passed bool
        server_info = Info(starting_load=setBool, last_updated=datetime.now())
        session.add(server_info)
        session.commit()

    session.close()


# Check info table to see if an insert is currently taking place
def checkLoading():
    session = Session()
    server_info_query = session.query(Info).filter(Info.id == 1)
    result = server_info_query.first()
    session.close()
    return result.starting_load

if __name__ == "__main__":
    getStreams()
