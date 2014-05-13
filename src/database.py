import MySQLdb
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime, insert, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

#HOST = 'web368.webfaction.com'
HOST = "127.0.0.1"
USER = 'fightwatch'
PASS = 'Thepassforthisdatabaseis_J0e_mysql12'
PORT = '3306'
DB = 'fightwatch'

engine = create_engine("mysql+mysqldb://" + USER + ":" + PASS + "@" + 
							HOST + ":" + PORT + "/" + DB)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Stream(Base):	
	__tablename__='streams'
	id = Column(Integer, primary_key=True)	
	game = Column(String(256), nullable=False)
	display_game = Column( String(256), nullable=False )
	url = Column(String(256), nullable=False)
	preview_location = Column(String(256), nullable=False)
	channel_name = Column(String(256), nullable=False)
	viewers = Column(String(256), nullable=False)

	def __repr__(self):
		return "<Stream(game='%s', display_game='%s', url='%s', \
				preview_location='%s', channel_name='%s', viewers='%s')>" % (self.game, 
				self.display_game, self.url, self.preview_location,	self.channel_name, self.viewers)

class Info(Base):
	__tablename__ = 'info'
	id = Column(Integer, primary_key=True)
	starting_load = Column(Boolean, nullable=False)
	last_updated = Column(DateTime, nullable=False)

	def __repr__(self):
		return "<Info(starting_load='%s', last_updated='%s'>" %	(self.starting_load, self.last_updated)	

def multiStreamInsert(list_of_dicts):	
	session = Session()	
	#Insert multiple values
	session.add_all(list_of_dicts)
	#Commit session
	session.commit()
	session.close()


def createSchema():
	Base.metadata.create_all(engine)

def getStreams():
	session = Session()
	for instance in session.query(Stream).order_by(Stream.game): 
		print instance.id, instance.game, instance.display_game
		
	session.close()


if __name__ == "__main__":		
	#Make sure the DB and table exists.
	#createSchema()
	TestInput = [
		Stream(game='Street Fighter', display_game='Street Fighter IV', url='http://google.com',
		preview_location='http://google.com/images.jpg', channel_name='EVO 2014 Let Go', viewers='12345' ),
		Stream(game='Street Fighter', display_game='Street Fighter IV', url='http://google.com',
		preview_location='http://google.com/images.jpg', channel_name='EVO 2014 Let Go', viewers='12345' ),
	]

	session = Session()	
	#multiStreamInsert(TestInput)	


#workon your_virtualenv #activate your virtualenv
#easy_install -U distribute #update distribute on your virtualenv
#pip install MySQL-python #install your package
#pip install MySQL-python