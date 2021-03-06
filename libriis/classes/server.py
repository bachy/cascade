#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Filename: server.py
# @Last modified by:   bach
# @Last modified time: 03-06-2017
# @License: GPL-V3

from __future__ import absolute_import, print_function, division, unicode_literals

import sys, os
from socket import socket
import socketserver
import http.server
import threading

class Server():
   def __init__(self, parent):

      self.parent = parent
      # find free port
      sock = socket()
      sock.bind(('', 0))

      self._port = sock.getsockname()[1]
      sock.close()

      # self.initial_cwd = os.getcwd()
      self.thread = threading.Thread(target=self.webserver)
      self.thread.daemon = True
      self.thread.start()
      # os.chdir(self.initial_cwd)

   def webserver(self):
      os.chdir(self.parent.cwd)
      self.httpd = http.server.HTTPServer(('', self.port), http.server.SimpleHTTPRequestHandler)
      self.httpd.serve_forever()
      print("serving at port", self._port)

   @property
   def port(self):
        return self._port

   def reload(self):
      # self.thread.shutdown()
      os.chdir(self.parent.cwd)
      # self.thread.start()
      # os.chdir(self.initial_cwd)
