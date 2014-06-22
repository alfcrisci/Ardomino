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
		
def main():

	idnode = sys.argv[1]
	typecom=sys.argv[2]
	indexcom= sys.argv[3]
	indexlist= sys.argv[4]
	indexpattern= sys.argv[5]
		
	indextemplate=indexlist+typecom+indexcom
	indexcomc=indexlist+typecom
	indexmodelhashtag=indexlist+typecom+indexcom
	
	Config_nodes = ConfigParser.ConfigParser()
	Config_nodes.read("biomino_nodes.ini")
	Config_social = ConfigParser.ConfigParser()
	Config_social.read("biomino_social.ini")
	Config_msg = ConfigParser.ConfigParser()
	Config_msg.read("biomino_msg.ini")
	
	id_nodes=str(Config_nodes.get('AOnode_ID',idnode))
	template = Template(str(Config_msg.get('AOmino_msg_conversation',indextemplate)))
	hashtagcoms = str(Config_msg.get('AO_comclass_hashtag',indexcomc))
	hashtagstates = str(Config_msg.get('AO_modelclass_hashtag',indexmodelhashtag))
	
	APP_KEY=str(Config_social.get('AOmino_oauth_consumer_key_tw',idnode))
	APP_SECRET=str(Config_social.get('AOnode_OA_consumer_secret_tw',idnode))
	OAUTH_TOKEN=str(Config_social.get('AOmino_OA_access_token_tw',idnode))
	OAUTH_TOKEN_SECRET=str(Config_social.get('AOmino_OA_access_token_secret_tw',idnode))
	twitter = Twython(APP_KEY, APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
	client_args = { "headers": {"accept-charset": "utf-8"}}
	
	
	message = template.substitute(idnode=id_nodes,hashtagcom=hashtagcoms,hashtagstate=hashtagstates)
	print message
	try:
		twitter.update_status(status=message.decode('latin-1').encode('utf-8'))
	except TwythonError as e:
		print e	
				  
if __name__ == '__main__':
     main()
	 
	 
