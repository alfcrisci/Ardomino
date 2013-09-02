#!/usr/bin/python
import sys,json
import MySQLdb 
result = {'success':'true','message':'The Command Completed Successfully'};

myjson = json.load(sys.stdin)

tair=myjson["tair"]
hrel=myjson["hrel"]
# mac=myjson["mac"]
# hrel=myjson["AO_IDnodes"]

# Begin json generation

print 'Content-Type: application/json\n\n'
json.dump(result, sys.stdout)


