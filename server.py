#!/usr/bin/python

###################################################################
# SENDKEY HANDLER 
# Special Thanks P'Bae for win32com API \(*3*)/
###################################################################

import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")

###################################################################
# WEB SERVER
# https://snipt.net/raw/f8ef141069c3e7ac7e0134c6b58c25bf/?nice
###################################################################

"""
Save this file as server.py
>>> python server.py 0.0.0.0 8001
serving on 0.0.0.0:8001

or simply

>>> python server.py
Serving on localhost:8000

You can use this to test GET and POST methods.

"""

import SimpleHTTPServer
import SocketServer
import logging
import cgi
import sys

if len(sys.argv) > 2:
    PORT = int(sys.argv[2])
    I = sys.argv[1]
elif len(sys.argv) > 1:
    PORT = int(sys.argv[1])
    I = ""
else:
    PORT = 8000
    I = ""

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        #logging.warning("======= GET STARTED =======")
        #logging.warning(self.headers)

        s = self.path[1:].strip()
        logging.warning("======= " + s + " =======")

        if s != 'favicon.ico':
            shell.sendKeys(s)
            shell.sendKeys("{Enter}")

        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        logging.warning("======= POST VALUES =======")
        for item in form.list:
            logging.warning(item)
        logging.warning("\n")
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "@rochacbruno Python http server version 0.1 (for testing purposes only)"
print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)
httpd.serve_forever()
