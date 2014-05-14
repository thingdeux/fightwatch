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
Base = declarative_base()
Session = sessionmaker(bind=engine)

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
	deleteAllStreams(session)
	#Insert multiple values
	session.add_all(list_of_dicts)
	#Commit then close session
	session.commit()
	session.close()

def createSchema():
	Base.metadata.create_all(engine)

def getStreams(session):		
	if checkLoading(session) == False:		
		dict_to_return = {}
		#Create a dictionary full of lists that have the 
		for instance in session.query(Stream).order_by(Stream.game):
			try:				
				dict_to_return[instance.game].append([
					{'stream_category': instance.game, 
					 'display_name': instance.display_game,
					 'url': instance.url,
					 'viewers': instance.viewers,
					 'preview_location': instance.preview_location,
					 'channel_name': instance.channel_name
					 }
					])				
			except:
				dict_to_return[instance.game] = [{'stream_category': instance.game, 
					 'display_name': instance.display_game,
					 'url': instance.url,
					 'viewers': instance.viewers,
					 'preview_location': instance.preview_location,
					 'channel_name': instance.channel_name
					 }]			 					

		return (dict_to_return)
	else:
		return False

		
	session.close()

def deleteAllStreams(session):
	session = Session()
	for instance in session.query(Stream):
		session.delete(instance)
	session.commit()	


def setLoading(setBool, session=Session() ):
	session = Session()
	#Check to see id(1) exists
	try:
		server_info_query = session.query(Info).filter(Info.id == 1)	
		result = server_info_query.first()
		result.starting_load = setBool
		if setBool == False:
			result.last_updated = datetime.now()
		session.commit()

	except:	
		#If it doesn't exist create it with the passed bool		
		server_info = Info(starting_load=setBool, last_updated=datetime.now())
		session.add(server_info)
		session.commit()

	session.close()

#Check info table to see if an insert is currently taking place
def checkLoading(session):
	server_info_query = session.query(Info).filter(Info.id == 1)	
	result = server_info_query.first()	
	return result.starting_load

def deleteCurrentStreams(session):
	session = Session()

if __name__ == "__main__":	
	#import cProfile	
	#cProfile.run('getStreams()')	
	print "Yup"


#workon your_virtualenv #activate your virtualenv
#easy_install -U distribute #update distribute on your virtualenv
#pip install MySQL-python #install your package
#pip install MySQL-python