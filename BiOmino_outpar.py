#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import sys
import re
from string import Template
import codecs
import ConfigParser
from peewee import *
from twython import Twython, TwythonError
from datetime import datetime, timedelta, time, date
from time import localtime, strftime
import ephem,math

SEC30 = timedelta(seconds=30)
fmt = "%H:%M"
	
def format_timedelta(duration):
	seconds =  duration.seconds
	hours = (seconds / 3600)  
	minutes = (seconds-hours*3600) / 60 	
	return '{} ore e {} minuti '.format(hours,minutes)

	
def main():

	idnode = sys.argv[1]
	typecom=sys.argv[2]
	typeoutpar= sys.argv[3]
	indexpattern= sys.argv[4]
		
	indextemplate=indexpattern+typecom+typeoutpar
	indexcomc=indexpattern+typecom
	
	
	Config_nodes = ConfigParser.ConfigParser()
	Config_nodes.read("biomino_nodes.ini")
	Config_social = ConfigParser.ConfigParser()
	Config_social.read("biomino_social.ini")
	Config_msg = ConfigParser.ConfigParser()
	Config_msg.read("biomino_msg.ini")
	
	id_nodes=str(Config_nodes.get('AOnode_ID',idnode))
	home = ephem.Observer()
	sun = ephem.Sun()
	home.lat = str(Config_nodes.get('AO_ID_lat',idnode))
	home.long = str(Config_nodes.get('AO_ID_lon',idnode))
	home.elevation =float(str(Config_nodes.get('AO_ID_elev',idnode)))
	sun.compute(home)
	nextrise = home.next_rising(sun)
	nextset = home.next_setting(sun)
	nextrisea= ephem.localtime(nextrise)
	nextseta= ephem.localtime(nextset)
	nextriseh=nextrisea.strftime(fmt)
	nextseth=nextseta.strftime(fmt)
	hours  = format_timedelta(nextset.datetime() - nextrise.datetime())
	template = Template(str(Config_msg.get('AOmino_msg_outpar_msg',indextemplate)))
	hashtagcoms = str(Config_msg.get('AO_comclass_hashtag',indexcomc))
	
	APP_KEY=str(Config_social.get('AOmino_oauth_consumer_key_tw',idnode))
	APP_SECRET=str(Config_social.get('AOnode_OA_consumer_secret_tw',idnode))
	OAUTH_TOKEN=str(Config_social.get('AOmino_OA_access_token_tw',idnode))
	OAUTH_TOKEN_SECRET=str(Config_social.get('AOmino_OA_access_token_secret_tw',idnode))
	twitter = Twython(APP_KEY, APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
	client_args = { "headers": {"accept-charset": "utf-8"}}
	
	if typeoutpar =='a':
		message = template.substitute(idnode=id_nodes,sunriseh=nextriseh,sunseth=nextseth,suntime=hours,hashtagcom=hashtagcoms)
	else:
		message = template.substitute(idnode=id_nodes,hashtagcom=hashtagcoms)
	print message
	try:
		twitter.update_status(status=message.decode('latin-1').encode('utf-8'))
	except TwythonError as e:
		print e	
				  
if __name__ == '__main__':
     main()
	 
	 
