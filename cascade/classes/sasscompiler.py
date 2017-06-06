#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   30-05-2017
# @Email:  bachir@figureslibres.io
# @Filename: sasscompiler.py
# @Last modified by:   bach
# @Last modified time: 03-06-2017
# @License: GPL-V3


import os
from PyQt5.QtCore import QFileSystemWatcher
import sass

class Compiler():
   def __init__(self,parent):
      self.parent = parent
      self.initWatching()
      self.compile_scss()
   # def directory_changed(path):
   #    print("Directory changed : %s" % path)

   def initWatching(self):
      self.refreshPaths()
      self.fs_watcher = QFileSystemWatcher(self.paths)
      # self.fs_watcher.directoryChanged.connect(self.directory_changed)
      self.fs_watcher.fileChanged.connect(self.compile_scss)

   def compile_scss(self):
      print("compiling sass")
      try:
         scss = sass.compile_file(str.encode(os.path.join(self.parent.cwd,'assets/css/main.scss')))
         with open(os.path.join(self.parent.cwd,'assets/css/main.css'), 'w') as fp:
            fp.write(scss.decode('utf8'))
      except Exception as e:
         print("Error compiling Sass", e)
         pass


   def refreshPaths(self):
      self.paths = [
         os.path.join(self.parent.cwd,'assets'),
         os.path.join(self.parent.cwd,'assets/css')
      ]
      # os.path.join(self.parent.cwd,'assets/css/styles.scss')
      for f in os.listdir(os.path.join(self.parent.cwd,'assets/css')):
         if f.endswith("scss"):
            self.paths.append(os.path.join(self.parent.cwd,'assets/css',f))

   def reload(self):
      print('Reload sass compiler')
      self.fs_watcher.removePaths(self.paths)
      self.refreshPaths()
      print('paths', self.paths)
      self.fs_watcher.addPaths(self.paths)
      print('files', self.fs_watcher.files())
      self.compile_scss()