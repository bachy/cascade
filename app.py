#!/usr/bin/python
# -*- coding: utf-8 -*-


# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 21-04-2017
# @License: GPL-V3

import sys, os

from socket import socket
import socketserver
import http.server
import threading

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, QUrl, QFileSystemWatcher, pyqtSlot
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QShortcut, QGridLayout, QLabel, QTabWidget, QHBoxLayout, QVBoxLayout, QSplitter, QSplitterHandle
# from PyQt5.QtNetwork import QNetworkProxyFactory, QNetworkRequest
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage, QWebView, QWebInspector

import sass

class Core():
   def __init__(self, parent=None):
      self.server = Server()
      self.compiler = Compiler()

class Server():

   def __init__(self, parent=None):

      # find free port
      sock = socket()
      sock.bind(('', 0))

      self._port = sock.getsockname()[1]
      sock.close()

      self.httpd = http.server.HTTPServer(('', self.port), http.server.SimpleHTTPRequestHandler)
      self.thread = threading.Thread(target=self.httpd.serve_forever)
      self.thread.start()
      print("serving at port", self._port)


   @property
   def port(self):
        return self._port


class Compiler():
   def __init__(self,parent=None):
      paths = [
         'assets',
         'assets/scss',
         'assets/scss/styles.scss'
      ]
      self.fs_watcher = QFileSystemWatcher(paths)
      # self.fs_watcher.directoryChanged.connect(self.directory_changed)
      self.fs_watcher.fileChanged.connect(self.compile_scss)
      self.compile_scss()

   # def directory_changed(path):
   #    print("Directory changed : %s" % path)

   def compile_scss(path = ""):
      print("compiling sass : %s" % path)
      scss = sass.compile_file(b'assets/scss/main.scss')
      with open('assets/scss/main.css', 'w') as fp:
         fp.write(scss.decode('utf8'))


class WebkitView(QWebView):
   def __init__(self, port):
      self.port = port
      self.view = QWebView.__init__(self)
      self.load(QUrl('http://localhost:'+str(self.port)))
      self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
      # self.settings().setAttribute(QWebSettings.PluginsEnabled, True)


class WebkitInspector(QWebInspector):
   def __init__(self, webkitview):
      super().__init__()
      self.webkitview = webkitview
      self.setPage(self.webkitview.page())
      # TODO: webkitinspector is disappearing when chaging tabs

class ViewTab(QWidget):
   def __init__(self, core):
      super(ViewTab, self).__init__()

      # self.grid = QGridLayout()
      hbox = QHBoxLayout()
      self.setLayout(hbox)


      # webviewbox = QVBoxLayout()
      vsplitter = QSplitter(QtCore.Qt.Vertical)

      self.webkitview = WebkitView(core.server.port)
      vsplitter.addWidget(self.webkitview)

      self.webkitinspector = WebkitInspector(self.webkitview)
      vsplitter.addWidget(self.webkitinspector)

      hsplitter = QSplitter(QtCore.Qt.Horizontal)
      hsplitter.addWidget(vsplitter)

      self.codeeditor = QLabel("Code Editor (SCSS & JS)")
      hsplitter.addWidget(self.codeeditor)

      hbox.addWidget(hsplitter)

   def onChanged(self, text):
      print("ViewTba Layout Changed")
      self.lbl.setText(text)
      self.lbl.adjustSize()


class MainWindow(QMainWindow):
   def __init__(self, core):
      super(MainWindow, self).__init__()

      self.setWindowFlags(QtCore.Qt.WindowTitleHint)
      # QtCore.Qt.CustomizeWindowHint
      # | QtCore.Qt.Tool
      #  | QtCore.Qt.FramelessWindowHint
      #  | QtCore.Qt.WindowTitleHint
      #  | QtCore.Qt.WindowStaysOnTopHint


      self.tabwidget = QTabWidget()

      # self.tabwidget.setStyleSheet("""
      #   .QWidget {
      #       border: 1px solid black;
      #       margin:0;
      #       padding:0;
      #       }
      #   """)

      self.viewtab = ViewTab(core)
      self.contenttab = QLabel("Content (markdown editor).")
      self.versiontab = QLabel("Version (git).")


      self.tabwidget.addTab(self.viewtab, "View")
      self.tabwidget.addTab(self.contenttab, "Content")
      self.tabwidget.addTab(self.versiontab, "Version")

      self.setCentralWidget(self.tabwidget)

      self.shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
      self.shortcut.activated.connect(self.on_quit)


      self.show()

   @pyqtSlot()
   def on_quit(self):
     print("Quit!")
     QCoreApplication.instance().quit()


def main():
   # app = QtCore.QCoreApplication(sys.argv)
   app = QApplication(sys.argv)
   core = Core()

   mainappwindow = MainWindow(core)

   sys.exit(app.exec_())



if __name__ == "__main__":
   main()
