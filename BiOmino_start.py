#!/usr/bin/python
# -*- coding: utf-8 -*- 

import shutil
import os
import stat  
import sys
import ConfigParser
import logging
import subprocess 
from StringIO import StringIO
from random import randint
from datetime import datetime, timedelta, time, date
from time import sleep
from apscheduler.scheduler import Scheduler
from peewee import *
import pymeteosalute

############################
# Read configuration's files
############################
	
Config = ConfigParser.ConfigParser()
Config.read("biomino_nodes.ini")
Config_msg = ConfigParser.ConfigParser()
Config_msg.read("biomino_msg.ini")

DSTDB =Config.get('AOmino_server_mysql_db','1')
DSTCGI=Config.get('AOmino_server_cgi_path','1') 
DBTYPE = Config.get('AOmino_db','1') 
DATABASE = Config.get('AOmino_SQLite_db','1') 
PYDUMPFILE= Config.get('AOmino_dump_file','1') 
PYUPFILE =Config.get('AOmino_update_file','1') 

pathfiledb=DSTDB+DATABASE
pathfilecgiupdate=DSTCGI+PYUPFILE
pathfilecgidump=DSTCGI+PYDUMPFILE

N_modelclass_int=int(Config_msg.get('AOmsg_indexes','N_modelclass'))
N_comclass_int=int(Config_msg.get('AOmsg_indexes','N_comclass'))
N_node_int=int(Config_msg.get('AOmsg_indexes','N_node'))
N_pattern_p_int=int(Config_msg.get('AOmsg_indexes','N_pattern_p'))
N_pattern_i_int=int(Config_msg.get('AOmsg_indexes','N_pattern_i'))
N_com_pattern_i=int(Config_msg.get('AOmsg_indexes','N_com_pattern_i'))
N_msg_c1_int=int(Config_msg.get('AOmsg_indexes','N_pattern_c1'))
N_msg_c2_int=int(Config_msg.get('AOmsg_indexes','N_pattern_c2'))
N_msg_c3_int=int(Config_msg.get('AOmsg_indexes','N_pattern_c3'))
N_msg_c4_int=int(Config_msg.get('AOmsg_indexes','N_pattern_c4'))
N_msg_c5_int=int(Config_msg.get('AOmsg_indexes','N_pattern_c5'))
N_msg_c6_int=int(Config_msg.get('AOmsg_indexes','N_pattern_c6'))
N_msg_c7_int=int(Config_msg.get('AOmsg_indexes','N_pattern_c7'))
N_e_class_int=int(Config_msg.get('AOmsg_indexes','N_e_class'))
N_AO_pattern_o=int(Config_msg.get('AOmsg_indexes','N_AO_pattern_o'))
N_AO_pattern_o=int(Config_msg.get('AOmsg_indexes','N_AO_pattern_o'))
N_AO_main_hashtags=int(Config_msg.get('AOmsg_indexes','N_AO_main_hashtags'))
N_AO_node_hashtags=int(Config_msg.get('AOmsg_indexes','N_AO_main_hashtags'))
N_AO_mentions_node=int(Config_msg.get('AOmsg_indexes','N_AO_mentions_node'))
N_AO_mentions_istitution=int(Config_msg.get('AOmsg_indexes','N_AO_mentions_istitution'))
N_AO_mentions_friends=int(Config_msg.get('AOmsg_indexes','N_AO_mentions_friends'))
N_AO_links_weather=int(Config_msg.get('AOmsg_indexes','N_AO_links_weather'))

############################
# Initizialise db
############################
# -*- coding: utf-8 -*- 

	
############################
# Function to instance db
############################
def copydb (DATABASE,dstdb):
	shutil.copy(DATABASE,dstdb)
	st = os.stat(pathfiledb)
	os.chmod(pathfiledb, st.st_mode | stat.S_IEXEC)
def copycgiup(PYUPFILE,dstcgi):
	shutil.copy(PYUPFILE,dstcgi)
	st = os.stat(pathfilecgiupdate)
	os.chmod(pathfilecgiupdate, st.st_mode | stat.S_IEXEC)
def copycgidump(PYDUMPFILE,dstcgi):
	shutil.copy(PYDUMPFILE,dstcgi)
	st = os.stat(pathfilecgidump)
	os.chmod(pathfilecgidump, st.st_mode | stat.S_IEXEC)



def init_db(mysql_db):
    	
	class BaseModel(Model):		
		class Meta:
			database = mysql_db
	  	  
	class AO_Login(BaseModel):
		AO_usr_name = CharField(null=True)
		AO_passwd = TextField(null=True)
		AOmino_data_pass = TextField(null=True)
			
	
		
	class AO_metadata(BaseModel):
			AO_ID_meta = CharField(null=True)
			AO_places = TextField(null=True)
			AO_Resp_name = TextField(null=True)
			AO_Resp_mail = TextField(null=True)
			AO_Resp_twitter = TextField(null=True)
			AO_Resp_phone = TextField(null=True)
			AO_ID_lon = CharField(null=True)
			AO_ID_lat = CharField(null=True)
			AO_ID_elev = CharField(null=True)
			AO_ID_address = TextField(null=True)
			AOmino_model = TextField(null=True)
			AOnode_environement= TextField(null=True)
	
	class AO_server(BaseModel):
			AOmino_server_cgi_path = TextField(null=True)
			AOmino_web_collect = TextField(null=True)
			AOmino_server_mysql_pass = TextField(null=True)
			AOmino_server_mysql_user = TextField(null=True)
			AOmino_server_mysql_port = TextField(null=True)
			AOmino_url_data = TextField(null=True)
			AOmino_SQLite_db_path = TextField(null=True)
			AOmino_SQLite_db = TextField(null=True)
		
			
	class AO_parameter(BaseModel):
			AOmino_sensors= CharField(null=True)
			AOParAvailab= CharField(null=True)
			AOPartype= CharField(null=True)
			AOParName= CharField(null=True)
			AOParUnit= CharField(null=True)
			AOParTag= CharField(null=True)
	
	class AO_DB(BaseModel):
			AO_ID = CharField(null=False)
			AODB_datetime=DateTimeField(null=False)
			AODB_date = CharField(null=False)
			AODB_time =CharField(null=False)
			AODB_year = CharField(null=False)
			AODB_month = CharField(null=False)
			AODB_data = CharField(null=False)
			AODB_h = IntegerField(null=False)
			tmp = FloatField(null=True)
			rh = FloatField(null=True)
			tdew = FloatField(null=True)
			tmrt = FloatField(null=True)
			rad = FloatField(null=True)
			press = FloatField(null=True)
			ati = FloatField(null=True)
			vv = FloatField(null=True)
			vdir= CharField(null=True)
			utci = FloatField(null=True)
			utci_c = FloatField(null=True)
			raduv= FloatField(null=True)
			vbatt= FloatField(null=True)
			wifipower= FloatField(null=True)
	
			
			class Meta:
				order_by = ('AODB_datetime',)
    
	############################
	# Create tables
	############################
	
	mysql_db.connect()
	
	AO_Login.create_table()
	AO_metadata.create_table()
	AO_parameter.create_table()	
	AO_DB.create_table()
	AO_server.create_table()
	
	############################
	# Create basic user
	############################
	
	basic= AO_Login.create( AO_usr_name='basic', AO_passwd='agromino')
	
	############################
	# Create basic user
	############################
	
	nodes=float(Config.get('AOmino_indexes','nodes'))+1
	users=float(Config.get('AOmino_indexes','users'))+1
	pars=float(Config.get('AOmino_indexes','pars'))+1
	
	i = 1
	while i < nodes:
		AO_metadata.create(AO_ID_meta=Config.get('AOnode_ID',str(i)),\
		AO_places=Config.get('AOnode_places',str(i)),\
		AO_Resp_name=Config.get('AO_Resp_name',str(i)),\
		AO_Resp_mail=Config.get('AO_Resp_mail',str(i)),\
		AO_Resp_twitter=Config.get('AO_Resp_twitter',str(i)),\
		AO_Resp_phone=Config.get('AO_Resp_phone',str(i)),\
		AO_ID_lat=Config.get('AO_ID_lat',str(i)),\
		AO_ID_lon=Config.get('AO_ID_lon',str(i)),\
		AO_ID_elev=Config.get('AO_ID_elev',str(i)),\
		AO_ID_address=Config.get('AO_ID_address',str(i)),\
		AOnode_environement=Config.get('AOnode_environement',str(i)),\
		AOmino_model=Config.get('AOmino_model',str(i))\
		)
		i = i + 1 
									  
	i = 1
	while i < users:
		AO_Login.create(AO_usr_name=Config.get('AO_usr_name',str(i)),\
		AO_passwd=Config.get('AO_passwd',str(i)),\
		AOmino_data_pass=Config.get('AOmino_data_pass',str(i)))
		i = i + 1 
	
	i = 1
	while i < pars:
		AO_parameter.create(AOParTag=Config.get('AOParTag',str(i)),\
		AOmino_sensors=Config.get('AOmino_sensors',str(i)),\
		AOParAvailab=Config.get('AOParAvailab',str(i)),\
		AOPartype=Config.get('AOPartype',str(i)),\
		AOParName=Config.get('AOParName',str(i)),\
		AOParUnit=Config.get('AOParUnit',str(i))
		)			   
		i = i + 1 
		
	AO_server.create(AOmino_SQLite_db=Config.get('AOmino_SQLite_db','1'),\
		AOmino_SQLite_db_path=Config.get('AOmino_SQLite_db_path','1'),\
		AOmino_url_data=Config.get('AOmino_url_data','1'),\
		AOmino_web_collect=Config.get('AOmino_web_collect','1'),\
		AOmino_server_mysql_host=Config.get('AOmino_server_mysql_host','1'),\
		AOmino_server_mysql_db=Config.get('AOmino_server_mysql_db','1'),\
		AOmino_server_mysql_port=Config.get('AOmino_server_mysql_port','1'),\
		AOmino_server_mysql_user=Config.get('AOmino_server_mysql_user','1'),\
		AOmino_server_mysql_pass=Config.get('AOmino_server_mysql_pass','1'),\
		AOmino_server_cgi_path=Config.get('AOmino_server_cgi_path','1'))
	#########################################################à
	
	mysql_db.close()   
############################
# Define job
############################


def send_parametric(idnode,typecom,indexcom,indexpattern,indexnameparam_1,indexnameparam_2):
    querydb=AO_DB.select().limit(1)
	for aodb in query:
			param_1s=str(aodb.tmp)
			param_2s=str(aodb.rh)	
	subprocess.call(['python', 'BiOmino_param.py',idnode,typecom,indexcom,indexpattern,indexnameparam_1,param_1s,indexnameparam_2,param_2s], shell=True)
 
def send_informative(idnode,typecom,indexcom,indexpattern):
    subprocess.call(['python', 'BiOmino_inform.py', idnode,typecom,indexcom,indexpattern], shell=True)
   
def send_conversation(idnode,typecom,indexcom,indexlist,indexpattern):
		if indexpattern == 'R':
			indexrandom='N_pattern_'+typecom+indexcom
			indexnew=str(randint(0,int(Config_msg.get('AOmsg_indexes',indexrandom))))
			subprocess.call(['python', 'BiOmino_convers.py', idnode, typecom, indexcom, indexlist,indexnew], shell=True)
			
		else:
			subprocess.call(['python', 'BiOmino_convers.py', idnode,typecom,indexcom,indexlist,indexpattern], shell=True)
    
def send_engagement(idnode,typecom,typengage,indexperiod,indexlisteng,indexlisthash):	
	subprocess.call(['python', 'BiOmino_engaged.py', idnode,typecom,typengage,indexperiod,indexlisteng,indexlisthash], shell=True)

    
 		
def cgi_manage():	
	copydb()
	copycgiup()
	copycgidump()
		
	
   
##############################################################

if __name__ == "__main__":
	
	#########################################################
	# db management
	
	db = SqliteDatabase(DATABASE, threadlocals=True)
	
	class AO_Login(Model):
		class Meta:
				database = db 
				
	db.connect()
	
	if not AO_Login.table_exists():
		init_db(db)
		print('OK database SQLite '+DATABASE+' installato!') 
	else:
		print('OK database SQLite '+DATABASE+' precedentemente installato!') 

	db.close()
	
	#cgi_manage()
	
	#########################################################
	# Scheduling
	
	sched = Scheduler()
	sched.configure({'apscheduler.daemonic': False})
	sched.start()        # start the scheduler
	
	job_param = sched.add_interval_job(send_parametric, seconds=10, args=['1', 'p', '3', '1', '1','2'])
	job_inform= sched.add_interval_job(send_informative, seconds=20, args=['1', 'i', '1', '1'])
	
	###############################################################################################################################à
	# Example of scheduling
	#job = sched.add_date_job(my_job, '2013-08-05 23:47:05', ['text'])
    #job = sched.add_interval_job(my_job, seconds=3,args=)
	#job = sched.add_cron_job(my_job, minute="*/15", args=['text'])
	
	while True:
		pass
