#!/usr/bin/env python
import FitBit
import yaml
import getopt
import sys


def usage():
	pass

if __name__ == '__main__':
	uname = ""
	passw = ""
	hname = ""
	dbnam = ""
	fname = ""
	conf = ""
	c = None
	try:
		opts,args = getopt.getopt(sys.argv[1:], "u:p:h:d:c:f:", ["config=","host=","user=",
									"pass=", "db=","file="])
	except getopt.GetoptError as err:
		print >> sys.stderr, str(err)
		usage()
		sys.exit(1)
	for o, a in opts:
		if o in ("-c", "--config"):
			conf = a
		elif o in ("-u", "--user"):
			uname = a
		elif o in ("-p", "--pass"):
			passw = a
		elif o in ("-h", "--host"):
			hname = a
		elif o in ("-d", "--db"):
			dbnam = a
		elif i in ("-f", "--file"):
			fname = a
		else:
			assert False, "unknown option"
	
	# end command parsing
	# load the config, but the options on the cli over-ride the config
	if len(conf) > 0:
		with open(conf,'r') as stream:
			c = yaml.load(stream)
	else:
		with open("config.yml", 'r') as stream:
			c = yaml.load(stream)
	if len(uname) == 0:
		uname = c['username']
	if len(passw) == 0:
		passw = c['password']
	if len(hname) == 0:
		hname = c['hostname']
	if len(dbnam) == 0:
		dbnam = c['database']
	if len(fname) == 0:
		fname = c['file']
						 	

	
	fb = FitBit
	fb.load_file(fname)
	fb.connect(uname,passw,hname,dbnam)
	fb.insert_data()
	fb.dbcommit()
	db.dbclose()
	
