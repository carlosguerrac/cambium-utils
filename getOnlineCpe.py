#!/usr/bin/python

import MySQLdb
import getpass
import sys
import telnetlib
import re
import socket

USER = "****"
PASSWD = "****"
PATH = "config_files"

def checkTelnetOpen(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    if result == 0:
       # print "Port is open"
       print >>sys.stderr, "host telnet port is open ", host
       return 1
    else:
       print >>sys.stderr, "fatal error host telnet disable ", host
    return 0

def telnetGetConfig(host, user, passwd):
    try:
       #tn = telnetlib.Telnet(host)
       print "**"
       tn = telnetlib.Telnet(host, timeout=10)
       tn.set_debuglevel(1)
       try:
          tn.read_until("login:")
          tn.write(user + "\n")
          tn.read_until("Password:")
          tn.write(PASSWD + "\n")
       except EOFError:
          print "Authentication to "+ self.telnet_host+" failed.\n"
          return None

       tn.write("config show\n")
       tn.read_until(b">")
       tn.write("exit\n")
       return tn.read_all()

    except socket.timeout:
        pass

    return None
# Open database connection
db = MySQLdb.connect("****t","****","****","*****" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "SELECT * FROM radioStatus \
       WHERE cpe_status = 'online'  \
       AND (product='ePMP 1000' OR product='ePMP Force 180') ORDER BY ip "

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      mac = row[0]
      ip = row[1]
      product = row[2]
      product_type = row[3]
      cpe_status = row[4]
      # Now print fetched result
      print "mac=%s,ip=%s,product=%s,type=%s, status=%s" % \
             (mac, ip, product, product_type, cpe_status )

      filename = "%s/%s.txt" % (PATH, ip)
      fn = open(filename,"w")
      if (checkTelnetOpen(ip, 23)):
          resultado =  telnetGetConfig(ip, USER, PASSWD)
          print "llegara aca"
      fn.write( resultado )
      fn.close()

except:
   pass
   #print "Error: unable to fecth data"

# disconnect from server
db.close()
