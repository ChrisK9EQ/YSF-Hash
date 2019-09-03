#!c:\python\python37\python.exe
import sys
import cgi, cgitb

# Copyright 2019 Chris Petersen, K9EQ
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Program to take a YSF Reflector name and determine the hash
# Input can either be from the command line or via a cgi-bin call
# Command line:
#	Enter the reflector name as the first argument as in CheckHasy.py "US MNWIS"
# cgi-bin
# 	Input name via the YSFReflectorName variable
#	cgi-bin will be used if there is no command line input
# Result is the reflector number

# Visit HamOperator.com for more information

# Revision history
# 0.1	Initial release
Rev = '0.1'	

if sys.stdin.isatty():  # Running from command line?
	cgibin = False
else:
	cgibin = True
	cgitb.enable() # Enable debugging for cgi-bin
	
def YSFHash(YSFName):
    hash = 0
    for c in YSFName:
        hash += c
        hash += (hash << 10)
        hash &= 0xffffffff  # Hash only works on 32 bit integers mask
        hash ^= (hash >> 6)
    # Finalize
    hash += (hash << 3)
    hash &= 0xffffffff  # Mask for 32-bit c integers
    hash ^= (hash >> 11)
    hash += (hash << 15)
    hash &= 0xffffffff
    hash = hash % 100000
    return(hash)

Error = False
htmlText = ""

if (cgibin == True):
	htmlText = "<p>" # Only add new line if running as cgi-bin
	try:
		print("Content-Type: text/html") # Output HTML header
		print()
	except:
		cgi.print_exception()
		Error = True
	form = cgi.FieldStorage()
	#if "YSFReflectorName" not in form:
		#print("<H2>Error<H2>")
		#print()
		#print("Enter YSF Reflector name up to 16 characters")
		#Error = True
	try:
		Name = form.getvalue('YSFReflectorName',"No Value Submitted")
	except:
		print("Must provide a YSF reflector name<p>")
		Error = True
else: # Command line
	try:
		Name = sys.argv[1]
	except:
		print("Must provide a YSF reflector name")
		sys.exit(1)

print("YSF Hasher " + Rev + " by K9EQ" + htmlText)
print("Reflector name: " + Name + htmlText)
if (Error == False):		
	Name = '{:16}'.format(Name)
	Name = bytearray(Name.encode())
	result = YSFHash(Name)
	print("Hash is: " + str(result))

if (cgibin == True):
	print("<p><H3>Press back on your browser to return to the previous screen</H3>")
