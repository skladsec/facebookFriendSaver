#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys, getopt, re, os
try:
	from splinter import Browser
except:
	print "Please install Splinter: http://splinter.readthedocs.org/en/latest/install.html"
	sys.exit();

import getpass
from splinter.request_handler.status_code import HttpResponseError

def main(argv):
	email = None
	txtipt = None
	socks = None
	socksPort = None
	try:
		opts, args = getopt.getopt(argv, "hi:m:S:P:",["port=","socks=","input=","mail=","help"])
	except:
		print "Use --help for help"
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print 'Usage %s options \n' % (os.path.basename(__file__))
			print '      -h, --help           This help'
			print '      -m, --mail           Your facebook login email'
			print '      -i, --input          Your input file name'
			print '      -S, --socks          Socks Proxy Address for Tor use'
			print '      -P, --port           Port Socks for Tor use'
			sys.exit()
		elif opt in ("-i","--input"):
			txtipt = arg
		elif opt in ("-m","--mail"):
			email = arg
		elif opt in ("-S","--socks"):
			socks = arg
		elif opt in ("-P","--port"):
			socksPort = arg
	if not email or not txtipt:
		print 'Use --help for help'
		sys.exit()

	password = getpass.getpass()

	if socks and socksProt:
		proxy_settings = {
		'network.proxy.type':1,
		'network.proxy.socks': socks,
		'network.proxy.socks_port': socksPort
		}

		browser = Browser('firefox',profile_preferences=proxy_settings)
	else:
		browser = Browser()
	# with Browser() as browser:
		browser.visit('https://m.facebook.com/')
		browser.fill("email",email);
		browser.fill("pass",password);
		browser.find_by_name("login").click()

		if browser.is_element_present_by_css('.login_error_box'):
			print 'The email and password didn\'t work.'
			sys.exit()
		
		try:
			fileipt = open(txtipt, 'r')
		except:
			sys.exit('Unable to open file %s' % txtipt)

		for line in fileipt:
			browser.visit(line)
			addButton = browser.find_link_by_text('Add Friend')
			if len(addButton) > 0:
				addButton[0].click()


if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except KeyboardInterrupt:
		sys.stdout.write('\nQuit by keyboard interrupt sequence!')
