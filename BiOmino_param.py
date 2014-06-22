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
	indexpattern= sys.argv[4]
	indexnameparam_1= sys.argv[5]
	param_1s= sys.argv[6]
	indexnameparam_2= sys.argv[7]
	param_2s= sys.argv[8]
	
	indextemplate=indexpattern+typecom+indexpattern
	indexcomc=indexpattern+typecom
	indexmodelhashtag=indexpattern+typecom+indexcom
	
	Config_nodes = ConfigParser.ConfigParser()
	Config_nodes.read("biomino_nodes.ini")
	Config_social = ConfigParser.ConfigParser()
	Config_social.read("biomino_social.ini")
	Config_msg = ConfigParser.ConfigParser()
	Config_msg.read("biomino_msg.ini")
	
	id_nodes=str(Config_nodes.get('AOnode_ID',idnode))
	template = Template(str(Config_msg.get('AOmino_msg_parametric',indextemplate)))
	hashtagcoms = str(Config_msg.get('AO_comclass_hashtag',indexcomc))
	hashtagstates = str(Config_msg.get('AO_modelclass_hashtag',indexmodelhashtag))
	nameparam_1s=str(Config_nodes.get('AOParNameshort',indexnameparam_1))
	nameparam_2s= str(Config_nodes.get('AOParNameshort',indexnameparam_2))
	unitpar_1s=str(Config_nodes.get('AOParUnit',indexnameparam_1))
	unitpar_2s=str(Config_nodes.get('AOParUnit',indexnameparam_2))
	
	APP_KEY=str(Config_social.get('AOmino_oauth_consumer_key_tw',idnode))
	APP_SECRET=str(Config_social.get('AOnode_OA_consumer_secret_tw',idnode))
	OAUTH_TOKEN=str(Config_social.get('AOmino_OA_access_token_tw',idnode))
	OAUTH_TOKEN_SECRET=str(Config_social.get('AOmino_OA_access_token_secret_tw',idnode))
	
	####################################################################################################
	# uncommnet for social job
	
	twitter = Twython(APP_KEY, APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
	client_args = { "headers": {"accept-charset": "utf-8"}}
	
	
	message = template.substitute(idnode=id_nodes,namepar_1=nameparam_1s,par_1=param_1s,unitpar_1=unitpar_1s,namepar_2=nameparam_2s,par_2=param_2s,unitpar_2=unitpar_2s,hashtagcom=hashtagcoms,hashtagstate=hashtagstates)
	print message
	try:
		twitter.update_status(status=message.decode('latin-1').encode('utf-8'))
	except TwythonError as e:
		print e	
				  
if __name__ == '__main__':
     main()
	 
	 
