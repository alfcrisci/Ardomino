#!/usr/bin/python
import json
import os
import sys
from peewee import *
from datetime import datetime, timedelta, time, date
import pymeteosalute

import cgi
import cgitb
cgitb.enable()
form   = cgi.FieldStorage()

############################################################
# Set missing data

tmpf=float('-99.9')
rhf=float('-99.9')
pvapf=float('-99.9')
tdewf=float('-99.9')
tmrtf=tmpf
vvf=float('0.5')
vdirf=float('-99.9')
atif=float('-99.9')
ati=float('-99.9')
utci=float('-99.9')
utci_c=float('-99.9')
raduv=float('-99.9')		
precipf=float('-99.9')			
radf=float('-99.9')
pressf=float('-99.9')
raduvf=float('-99.9')
vbattf=float('-99.9')
wifipowerf=float('-99.9')
     	  
############################################################
# Retrieve GET parameter 

ID=form.getvalue("ID")
tmpf=float(form.getvalue("tmp"))
rhf=float(form.getvalue("rh"))
tmrtf=float(form.getvalue("tmrt"))
#radf=float(form.getvalue("rad"))
#precf=float(form.getvalue("pp"))
#pressf=float(form.getvalue("press"))
vvf=float(form.getvalue("vv"))
vdirf=float(form.getvalue("vdir"))
#raduvf=float(form.getvalue("raduv"))
vbattf=float(form.getvalue("vbatt"))
login=form.getvalue("login")

############################################################
# Set wind velocity to 0.5 m/sec
 
vvf=float('0.5')

############################################################
# Calculate missing parameter

p_vapf=pymeteosalute.p_vap(tmpf,rhf)
tdewf=pymeteosalute.dewpoint(tmpf,rhf)
utcif=pymeteosalute.utci(tmpf,tmpf,vvf,rhf)
utci_cf=pymeteosalute.utci_class_7(tmpf,tmrtf,vvf,rhf)
atif=pymeteosalute.steadman_outdoor_shade(tmpf,rhf,vvf)

############################################################
# set path of sqlite db

DATABASE = '/home/salute/social_network/biomino/biomino.db'

############################################################
# Peewee instancing
 
db = SqliteDatabase(DATABASE, threadlocals=True)

class Biomino(Model):		
	class Meta:
		database = db

class AO_Login(Biomino):
	AO_usr_name = CharField()
	AO_passwd = TextField()

class AO_parameter(Biomino):
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
				
############################################################
# Peewee instancing

db.connect()

############################################################
# Peewee instancing

ora = datetime.now()

utenteno='''<html>
<head><title>Agromino data service</title></head>
<body>
<p>Utente non accreditato</p>
</body>
</html>
'''
	
datiok='''<html>
<head><title>Agromino data service</title></head>
<body>
<p>Stringa dati accettata</p>
</body>
</html>
'''

datinook='''<html>
<head><title>Agromino data service</title></head>
<body>
<p>Stringa dati non accettata</p>
</body>
</html>
'''

print "Content-Type: text/html"	
print ""					
		
try:
	user = AO_Login.get(AO_usr_name = login)
	
except:
	print utenteno
	db.close()
	sys.exit(0)
  
try:
	post = AO_DB.create(AO_ID=ID,AODB_datetime=ora,AODB_date =ora.strftime("%Y-%m-%d"),AODB_time = ora.strftime("%H:%M"),AODB_year = ora.strftime("%Y"),AODB_month = ora.strftime("%m"),AODB_data = ora.strftime("%d"),AODB_h = int(ora.hour),tmp = tmpf,rh = rhf,pvap=p_vapf,tdew=tdewf,tmrt=tmrtf,vv=vvf,vdir= vdirf,ati = atif,utci = utcif,utci_c = utci_cf,raduv = raduvf,rad = radf,precip = precipf,press = pressf,vbatt= vbattf,wifipower= wifipowerf)
	db.close()	
	print ora,"Utente: ",user.AO_usr_name,datiok
   
except:
	print ora,"Utente: ",user.AO_usr_name, datinook
	db.close()

   