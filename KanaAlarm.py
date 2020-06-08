#!/usr/bin/env python

import os
import time
import sys
import json

import webbrowser

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QHBoxLayout, QScrollArea, QVBoxLayout, QGroupBox, QGridLayout, QAction, QLabel, QWidget, QLineEdit, QComboBox, QPushButton, QCheckBox, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QProcess
from PyQt5.QtGui import QIcon, QPixmap

from config import JsonConfig
from youtube import Channel

import notify2
CONFIGPATH = "config.json"

# Todo 
# Logging
# Config
# Clean up imports
# Make Variables that sould be consts consts ex: languagePath (also change it to defaultLanguagePath)
# Make a language select popup on first run? Maybe 
# Notifications

# Problems:
# I built most of this in a way that can be expanded to more youtube channels but someparts of it are still specific to Kana so it just ruins the point of it being expandable. It doesn't really effect me tho.

class KanaAlarm(QMainWindow):
	
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):
		self.win = QWidget()
		
		self.notify = notify2.init("KanaAlarm")
		
		self.configOptions = [
			"defaultLanguagePath",
			"streamerId",
			"streamerName",
			"streamerPfp",
			"updateTime"
		]
	
		self.config = JsonConfig(self.resource_path(CONFIGPATH))
		self.config.loadConfig()

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.checkIfLive)
		self.timer.setInterval(self.config.getOption(self.configOptions[4]))
		self.timer.start()

		self.languagePath = self.config.getOption(self.configOptions[0])

		self.textFields = [
			"title",
			"fileMenuTitle",
			"languageMenuTitle",
			"languageMenuEnglish",
			"languageMenuJapanese",
			"streamerName",
			"buttonOffline",
			"buttonOnline"
		]

		self.localizedText = JsonConfig(self.resource_path(self.languagePath))
		
		try:
			self.localizedText.loadConfig()
		except:
			print("Malformed Laguage file path. Loading english default")
			self.localizedText.configFilePath=self.resource_path("lang/en_US.json")
			self.localizedText.loadConfig()

		self.kana = Channel(name=self.config.getOption(self.configOptions[2]),id=self.config.getOption(self.configOptions[1]),pfp=self.config.getOption(self.configOptions[3]),prevStreamingStatus=False)

		menubar = self.menuBar()
		filemenu = menubar.addMenu(self.localizedText.getOption(fieldName=self.textFields[1]))
		#filemenu.addAction(quitAction)

		englishAction = QAction(self.localizedText.getOption(fieldName=self.textFields[3]),self)
		englishAction.setShortcut("Ctrl-e")
		englishAction.triggered.connect(self.setLanguageToEnglish)
		
		japaneseAction = QAction(self.localizedText.getOption(fieldName=self.textFields[4]),self)
		japaneseAction.setShortcut("Ctrl-e")
		japaneseAction.triggered.connect(self.setLanguageToJapanese)

		languageMenu = menubar.addMenu(self.localizedText.getOption(fieldName=self.textFields[2]))
		languageMenu.addAction(englishAction)
		languageMenu.addAction(japaneseAction)
		
		self.mainlayout = QVBoxLayout()
		
		self.pfp = QLabel()
		pixmap = QPixmap(self.config.getOption(self.configOptions[3]))
		self.pfp.setAlignment(Qt.AlignCenter)
		self.pfp.setPixmap(pixmap)
		self.mainlayout.addWidget(self.pfp)
		
		self.streamerLabel = QLabel(text=self.localizedText.getOption(fieldName=self.textFields[5]))
		self.streamerLabel.setAlignment(Qt.AlignCenter)
		self.mainlayout.addWidget(self.streamerLabel)
		
		if self.kana.streamingStatus: # Will prob change this because idk if this is actually a good system
			self.statusButton = QPushButton(text=self.localizedText.getOption(fieldName=self.textFields[7]))
		else:
			self.statusButton = QPushButton(text=self.localizedText.getOption(fieldName=self.textFields[6]))

		self.statusButton.clicked.connect(self.openLiveStream)

		self.mainlayout.addWidget(self.statusButton)
		
		self.win.setLayout(self.mainlayout)
		
		self.setCentralWidget(self.win)
		
		self.setWindowTitle(self.localizedText.getOption(fieldName=self.textFields[0])) 
		
		self.checkIfLive()
		
		self.show()
		
	def checkIfLive(self):
		
		print("CheckIfLive is running")
		
		self.kana.check_live()
		
		if self.kana.streamingStatus == True and self.kana.prevStreamingStatus == False:
			self.showNotification(msg="Kana is now live!")
			self.kana.prevStreamingStatus = True
		elif self.kana.streamingStatus == False and self.kana.prevStreamingStatus == True:
			print("kana is not offline")
			self.kana.prevStreamingStatus = False
	
	def setLanguageToEnglish(self):
		
		self.config.setOption(self.configOptions[0],"lang/en_US.json") # Replace this hardcoded path with variables loaded from config 
		
		self.config.saveConfig()
		
	def setLanguageToJapanese(self):
		
		self.config.setOption(self.configOptions[0],"lang/ja_JP.json") # Replace this hardcoded path with variables loaded from config 
		
		self.config.saveConfig()

	def showNotification(self,title=None,msg=None):
		
		self.notify = notify2.Notification(msg)
		self.notify.show()
		
	def openLiveStream(self): # Should this be apart of the channel class for youtube? idk. May move this later
		if self.kana.streamingStatus:
			for videos in self.kana.videoid:
				webbrowser.open("https://www.youtube.com/watch?v=" + videos)
		else:
			print("Not live")

	# Funtion that converts a path to a reletive path for when pyinstaller packages everything
	def resource_path(self,relative_path):
		if hasattr(sys, '_MEIPASS'):
			return os.path.join(sys._MEIPASS, relative_path)
		return os.path.join(os.path.abspath("."), relative_path)

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = KanaAlarm()
	sys.exit(app.exec_())
