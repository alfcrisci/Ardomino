#!/usr/bin/python
# -*- coding: utf-8 -*- 

import urllib2,StringIO,csv,json,os,sys
from string import Template
from peewee import *
from datetime import datetime, timedelta, time, date

import cgi
import cgitb
cgitb.enable()
form   = cgi.FieldStorage()
login=form.getvalue("login")


template = Template("{ ${response}:${name} }")

DATABASE = '/home/salute/social_network/biomino/biomino.db'

db = SqliteDatabase(DATABASE)

class Biomino(Model):		
		class Meta:
			database = db

class AO_Login(Biomino):
	AO_usr_name = CharField()
	AO_passwd = TextField()


db.connect()

print "Content-Type: application/json;"	
print ""
	
try:
	user = AO_Login.get(AO_usr_name = login)
except:
	print template.substitute(dict(response='"Response"',name='"Utente non accreditato"'))
	db.close() 
	exit(0)
try:
	url = 'http://149.139.8.55/cgi-bin/biomino_dump.py?login='+login
	response = urllib2.urlopen(url).read()
	output = StringIO.StringIO(response)
	reader = csv.DictReader(output, fieldnames= ( "ID_node","date","time","year","month","data","hour","tmp","rh","pvap","tdew","tmrt","vv","vdir","ati","utci","utci_c","raduv","precip","rad","press","vbatt","wifipower"))
	keys=next(reader)
	out = "[\n\t" + ",\n\t".join([json.dumps(row,sort_keys=True,indent=4) for row in reader]) + "\n]"
	print out

	
except:
	print template.substitute(dict(response='"Response"',name='"Retrieval dati non disponibile."'))

db.close() 


