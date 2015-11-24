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
	txtopt = None
	profile = None
	self = None
	socks = None
	socksPort = None
	try:
		opts, args = getopt.getopt(argv, "ho:m:p:s:S:P:",["port=","socks=","self=","profile=","output=","mail=","help"])
	except:
		print "Use --help for help"
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print 'Usage %s options \n' % (os.path.basename(__file__))
			print '      -h, --help           This help'
			print '      -m, --mail           Your facebook login email'
			print '      -o, --output         Your output file name'
			print '      -p, --profile        Profile to capture friends(name after facebook.com/)'
			print '      -s, --self           Your profile name(name after facebook.com/)'
			print '      -S, --socks          Socks Proxy Address for Tor use'
			print '      -P, --port           Port Socks for Tor use'
			sys.exit()
		elif opt in ("-o","--output"):
			txtopt = arg
		elif opt in ("-m","--mail"):
			email = arg
		elif opt in ("-p","--profile"):
			profile = arg
		elif opt in ("-s","--self"):
			self = arg
		elif opt in ("-S","--socks"):
			socks = arg
		elif opt in ("-P","--port"):
			socksPort = arg
	if not email or not txtopt or not self:
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
			fileopt = open(txtopt, 'a')
		except:
			sys.exit('Unable to open file %s' % txtopt)

		if not profile:
			browser.find_link_by_text("Profile").click()
			print 'Accessing profile at %s\n' % browser.url
			browser.find_link_by_text("Friends").click()
			print 'Accessing friends at %s\n' % browser.url
		else:
			url = 'https://m.facebook.com/%s/friends?refid=17' % profile
			print 'Accessing profile friends at %s\n' % url
			browser.visit(url)
		friends = browser.find_by_css('a')
		notList = ["/a/mobile/friends/add_friend.php","language.php","/help/","/settings/","/pages/","/bugnub/","/policies/","/logout","/home","/friends","/messages/","/notifications.php","/buddylist.php","/menu/","/photo.php","/mbasic/","%s"%profile,"%s"%self]
		for friend in friends:
			if all([x not in friend['href'] for x in notList ]):
				fileopt.write('%s\n' % friend['href'])
				print '%s' % friend.value

		while browser.is_element_present_by_css("#m_more_friends"):
			browser.find_by_css('#m_more_friends a').first.click()		
			friends = browser.find_by_css('a')
			for friend in friends:
				if all([x not in friend['href'] for x in notList ]):
					fileopt.write('%s\n' % friend['href'])
					print '%s' % friend.value

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except KeyboardInterrupt:
		sys.stdout.write('\nQuit by keyboard interrupt sequence!')
