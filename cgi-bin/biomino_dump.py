#!/usr/bin/python
# -*- coding: utf-8 -*- 

import json
import os
import sys
from string import Template
from peewee import *
from datetime import datetime, timedelta, time, date

import cgi
import cgitb
cgitb.enable()
form   = cgi.FieldStorage()
login=form.getvalue("login")

template = Template("<html><body><h2>${name}</h2></body></html>")

# change absolute path where sqlite db is instanced

DATABASE = '/home/salute/social_network/biomino/biomino.db'

db = SqliteDatabase(DATABASE)

class Biomino(Model):		
		class Meta:
			database = db

class AO_Login(Biomino):
	AO_usr_name = CharField()
	AO_passwd = TextField()

class AO_parameter(Biomino):
			AO_ID_meta= CharField(null=True) 			
			AOmino_sensors= CharField(null=True)
			AOParAvailab= CharField(null=True)
			AOPartype= CharField(null=True)
			AOParName= CharField(null=True)
			AOParUnit= CharField(null=True)
			AOParTag= CharField(null=True)
				
class AO_DB(Biomino):
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
			pvap = FloatField(null=True)
			tdew = FloatField(null=True)
			tmrt = FloatField(null=True)
			vv = FloatField(null=True)
			vdir= CharField(null=True)
			ati = FloatField(null=True)
			utci = FloatField(null=True)
			utci_c = FloatField(null=True)
			raduv= FloatField(null=True)		
			precip = FloatField(null=True)
			rad = FloatField(null=True)
			press = FloatField(null=True)
			vbatt= FloatField(null=True)
			wifipower= FloatField(null=True)
			
			class Meta:
				order_by = ('AODB_datetime',)
				

db.connect()

print "Content-Type: text/plain;"	
print ""
	
try:
	user = AO_Login.get(AO_usr_name = login)
except:
	print template.substitute(dict(name='Utente non accreditato'))

try:
	query = (AO_DB.select())
	print 'ID_node,date,time,year,month,data,hour,tmp,rh,pvap,tdew,tmrt,vv,vdir,ati,utci,utci_c,raduv,precip,rad,press,vbatt,wifipower'
	for aodb in query:
		temp=str(aodb.AO_ID)+','
		     +str(aodb.AODB_date)+','+\
		     str(aodb.AODB_time)+','+str(aodb.AODB_year)+','+str(aodb.AODB_month)+','+\
			 str(aodb.AODB_data)+','+str(aodb.AODB_h)+','+\
			 str(aodb.tmp)+','+str(aodb.rh)+','+str(aodb.pvap)+','+str(aodb.tdew)+','+\
			 str(aodb.tmrt)+','+str(aodb.vv)+','+str(aodb.vdir)+','+str(aodb.ati)+','+str(aodb.utci)+','+str(aodb.utci_c)+\
			 str(aodb.raduv)+','+str(aodb.precip)+','+str(aodb.rad)+','+str(aodb.press)+','+\
			 str(aodb.vbatt)+','+str(aodb.wifipower)
		print temp
		
except:
	print template.substitute(dict(name='retrieval dati non disponibile.'))

db.close() 




			


