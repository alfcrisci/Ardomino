#!/usr/bin/python

import MySQLdb 
import sys
import ConfigParser


					
AOmino_server_sql='CREATE TABLE IF NOT EXISTS AOmino_server ( AOhost varchar(64) PRIMARY KEY, \
                       AOport smallint(5) unsigned , \
                       AOname varchar(64) , \
                       AOuser varchar(64) , \
                       AOpassword varchar(64) , \
                       AOschema varchar(64) , \
                       AO_url_data varchar(128) , \
                       AO_query_data varchar(128) ,\
					   )'

AOmino_nodes_sql='CREATE TABLE IF NOT EXISTS ( AOnode_ID varchar(64)  PRIMARY KEY , \
                                               AOnode_names varchar(64) , \
                                               AOnode_places varchar(128) , \
                                               AOnode_coords_lat float default NULL,\
                                               AOnode_coords_lon float default NULL,\
                                               AOnode_coords_elevation smallint(5) default NULL, \
                                               AOnode_environementvarchar(64) , \
											   AOnode_MAC varchar(64) default NULL,\
                                              )'
					   
AOmino_data_sql  ='CREATE TABLE IF NOT EXISTS ard_bot_data ( AOnode_ID  varchar(64), \
                                                             time_m datetime, \
                                                             year smallint(5) unsigned default NULL, \
                                                             month tinyint(3) unsigned default NULL, \
                                                             day tinyint(3) unsigned default NULL, \
                                                             hour tinyint(3) unsigned default NULL, \
						                                     stateofday varchar(64) default NULL, \
                                                             datavalue float default NULL,\
						                                     dataclassname varchar(64) default NULL,\
															 dataparname varchar(64) default NULL,\
						                                     battery smallint(5) unsigned default NULL, \
						                                     )'	


AOmino_hard_soft_sql  ='CREATE TABLE IF NOT EXISTS AOmino_hard_soft ( AOnode_ID  varchar(64), \
                                                             AO_sensors_sensor varchar(64), \
                                                             AO_sensors_ref varchar(64), \
                                                             AO_shield varchar(64), \
                                                             AO_shield_ref varchar(64), \
                                                             AO_wifi varchar(64), \
                                                             AO_wifi_ref varchar(64), \
                                                             AO_github_repo varchar(64), \
                                                             AO_maintainer varchar(64), \
                                                             AO_tech_contact varchar(64),\
															 )'	

AOmino_parameters_sql  ='CREATE TABLE IF NOT EXISTS AOmino_parameters ( AOnode_ID  varchar(64), \
                                                             AOParDesc varchar(64), \
                                                             AOParTag varchar(64), \
                                                             AO_shield varchar(64), \
                                                             AOParAvailab varchar(64), \
                                                             AOParMap varchar(64), \
                                                             AO_wifi_ref varchar(64), \
                                                             AO_github_repo varchar(64), \
                                                             AO_maintainer varchar(64), \
                                                             AO_tech_contact varchar(64),\
															 )'	

AOmino_model_sql  ='CREATE TABLE IF NOT EXISTS AOmino_model ( AOnode_ID  varchar(64), \
                                                              AOModelTag varchar(64), \
                                                              AOModelDesc varchar(255), \
                                                              AOModelRef varchar(255), \
                                                              AOModelSoftware varchar(64), \
                                                              AOModelRepo varchar(64), \
                                                             )'

															 
AOmino_socialconn_sql  ='CREATE TABLE IF NOT EXISTS AOmino_model ( AOnode_ID  varchar(64), \
                                                                   AOnode_user_tw varchar(64), \
                                                              AOModelDesc varchar(255), \
                                                              AOModelRef varchar(255), \
                                                              AOModelSoftware varchar(64), \
                                                              AOModelRepo varchar(64), \
                                                             )'															 
															 
															 
[AOmino_socialconn]

AOnode_user_tw:["FirenzeDuomo","Trento MUSE"]
AOnode_app_tw:["",""]
AOnode_oauth_consumer_key_tw:["",""]
AOnode_oauth_consumer_secret_tw:["",""]
AOnode_oauth_access_token_tw:["",""]
AOnode_oauth_access_token_secret_tw:["",""]
AOnode_user_fb:["",""]
AOnode_pw_fb:["",""]
AOnode_app_fb:["",""]
AOnode_key_fb:["",""]
AOnode_gmail_user:["",""]
AOnode_gmail_pw:["",""]

[AOmino_indexclasses]

AOindexclasscode:['S1',
                  'S2',
                  'S3',
                  'S4',
                  'S5',
                  'S6',
                  'S7']

AOindexclassnoun:['molto freddo',
                  'freddo',
                  'freddo leggero',
                  'stato neutro',
                  'leggero caldo',
                  'caldo',
                  'molto caldo']

[AOmino_comclasses]

AOcomclasscode:['A',
                'B',
                'C',
                'D']

AOcomclass:['physical',
            'modelled_perception',
            'sintax_builded',
            'user_designed',
            'outparametric']


AOcomclass_desc:['predefined patternized message self describing values of data in terms of time and measured parameters',
                 'predefined sentences/patterns indicate the noun of data in predefined index/model classes  (i.e: biometeorological actual state) ',
                 'modular lexical patterns giving the sense  troughout an affirmation  on the state indicated by  data index classes ',
                 'ranked predefined sentence sets linked close topic related  textual expression previosly mapped during  crowd audit in social media',
                 'predefined sentence sets linked close topic for community building and contextual data engagement, indicate useful relate links and mentions'
                 ]

AOcomclasshash:['#RTD',
                '#MPD',
                '#SPD',
                '#USD',
				'#OUT'
				]


[AOmino_outparametric]

[AOmino_hashtags]

AOhashtag_gen=#Ardomino
AOhash_nodes=:['#FirenzeDuomo","#TrentoMUSE"]

[AOmino_mentions]
AOmention_node=:['#FirenzeDuomo","#TrentoMUSE"]
AOmention_istitutional=:['#FirenzeDuomo","#TrentoMUSE"]
AOmention_friends=:['#FirenzeDuomo","#TrentoMUSE"]

[AOmino_links]

															 
ARDOMINO_BOTDESC_TABLE ='CREATE TABLE IF NOT EXISTS ard_bot_desc ( AOnode_ID varchar(64)  PRIMARY KEY , \
                        place varchar(64), \
                        address_loc varchar(255), \
                        host_istitution varchar(255), \
                        lat decimal(6,3) default NULL,\
                        lon decimal(6,3) default NULL,\
                        elevation smallint(6) default NULL,\
                        tw_service varchar(64), \
                        type_dataconn varchar(64), \
                        n_sensors smallint(6), \
                        channel_used varchar(64), \
                        tw_user varchar(64), \
                        tw_service varchar(64), \
                        description varchar(255), \
                        updated datetime default NULL \
                     )'

				 
					


ARDOMINO_BOT_SOCIAL ='CREATE TABLE IF NOT EXISTS ard_bot_social ( idstr varchar(128) PRIMARY KEY, \
                    channel_used varchar(64), \
				    ID varchar (128), \
				    tw_user varchar (64),\
				    searchterm varchar (64), \
                    type_msg varchar(64), \					
					updated datetime default NULL,\
					type_msg varchar(64), \
					 text varchar(255),\
						id_text varchar(64) default NULL, \
						created_at varchar(64) datetime NULL, \
						lang varchar(3) default NULL, \
						place_country_code varchar(64) default NULL, \
						retweet_count varchar(64) default NULL, \
						place_full_name varchar(64) default NULL, \
						geolon decimal(6,3) default NULL, \
						geolat decimal(6,3) default NULL, \
						source varchar(64) default NULL, \
						user_id int default NULL, \						
						user_screen_name varchar(64) default NULL, \
						user_name varchar(64) default NULL, \
						user_created_at varchar(64) default NULL, \
						user_followers_count int default NULL, \
						user_friends_count int default NULL, \
						user_location varchar(128) default NULL, \
						user_statuses varchar(128) default NULL, \
						user_profile_image_url varchar(255) default NULL, \
						user_description varchar(255) default NULL \             
					)'
						
					 
					 


					 
def initialize_db(db_user, db_password, db_hostname, 
                  db_name_input, db_name_output):
    """
    """
    iconn = None
    oconn = None
      
    try:
        print('Connecting with %s database' % db_name_input)
        iconn = MySQLdb.connect(user=db_user, passwd=db_password, 
                                host=db_hostname, db=db_name_input)
        print('Connected')
    except MySQLdb.OperationalError, e:
        print 'Error connecting with input database. MySQL error. %s' % str(e.args)
        
    
    try:
        print('Creating output database %s' % db_name_output)
        cursor=iconn.cursor()
        cursor.execute('CREATE IF NOT EXISTS DATABASE %s' % db_name_output)
        cursor.close()
        print('Output database %s initialized' % db_name_output)
        
        oconn = MySQLdb.connect(user=db_user, passwd=db_password, 
                                host=db_hostname, db=db_name_output)
        cursor=oconn.cursor()        
        cursor.execute(ARDOMINO_BOTDESC_TABLE)
		cursor.execute(ARDOMINO_DATA_TABLE)
        cursor.close()
        print('Summary table initialized')
		iconn.close()
		oconn.close()
    except MySQLdb.OperationalError, e:
        print 'Error creating output database. MySQL error. %s' % str(e.args)
		sys.exit(0)
        
    return

def fill_db(db_user, db_password, db_hostname, 
                  db_name_input, db_name_output):

    return oconn				  
				  
if __name__ == "__main__":

Config = ConfigParser.ConfigParser()
Config.read("ardomino.ini")

initialize_db('root','laquerce','localhost','ardomino','ardomino')

try:
    print('Connecting with %s database' % db_name_input)
    iconn = MySQLdb.connect(user=db_user, passwd=db_password, host=db_hostname, db=db_name_input)
    print('Connected')
except MySQLdb.OperationalError, e:
        print 'Error connecting with input database. MySQL error. %s' % str(e.args)