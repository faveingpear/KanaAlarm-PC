#!/usr/bin/env python

import os
import time
import sys
import json

import webbrowser

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QHBoxLayout, QScrollArea, QVBoxLayout, QGroupBox, QGridLayout, QAction, QLabel, QWidget, QLineEdit, QComboBox, QPushButton, QCheckBox, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QProcess
from PyQt5.QtGui import QIcon, QPixmap

from language import Language
from youtube import Channel

# These will call be loaded from a config file later aka tomarrow
KANANAME = "Kaniko Kana"
KANAID = "UC-1b52dI6MuR5BNLQj2FvFg"
KANAPFP = "https://yt3.ggpht.com/a/AATXAJwB7g1Vtb0zDrynG9BK-Z99QuZ8MBYDLAwZxw=s100-c-k-c0xffffffff-no-rj-mo"

class KanaAlarm(QMainWindow):
	
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):
		self.win = QWidget()

		self.languagePath = "lang/en_US.json" # Will be loaded from a config file later

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

		self.localizedText = Language(self.resource_path(self.languagePath))
		self.localizedText.loadLanguageData()


		self.kana = Channel(name=KANANAME,id=KANAID,pfp=KANAPFP)

		self.kana.check_live()

		menubar = self.menuBar()
		filemenu = menubar.addMenu(self.localizedText.getText(fieldName=self.textFields[1]))
		#filemenu.addAction(quitAction)

		englishAction = QAction(self.localizedText.getText(fieldName=self.textFields[3]),self)
		englishAction.setShortcut("Ctrl-e")
		#englishAction.triggered.connect(self.setLanguageToEnglish)
		
		japaneseAction = QAction(self.localizedText.getText(fieldName=self.textFields[4]),self)
		japaneseAction.setShortcut("Ctrl-e")
		#japaneseAction.triggered.connect(self.setLanguageToJapanese)

		languageMenu = menubar.addMenu(self.localizedText.getText(fieldName=self.textFields[2]))
		languageMenu.addAction(englishAction)
		languageMenu.addAction(japaneseAction)
		
		self.mainlayout = QVBoxLayout()
		
		self.streamerLabel = QLabel(text=self.localizedText.getText(fieldName=self.textFields[5]))
		self.streamerLabel.setAlignment(Qt.AlignCenter)
		self.mainlayout.addWidget(self.streamerLabel)
		
		if self.kana.streamingStatus: # Will prob change this because idk if this is actually a good system
			self.statusButton = QPushButton(text=self.localizedText.getText(fieldName=self.textFields[7]))
		else:
			self.statusButton = QPushButton(text=self.localizedText.getText(fieldName=self.textFields[6]))

		self.statusButton.clicked.connect(self.openLiveStream)

		self.mainlayout.addWidget(self.statusButton)
		
		self.win.setLayout(self.mainlayout)
		
		self.setCentralWidget(self.win)
		
		self.setWindowTitle(self.localizedText.getText(fieldName=self.textFields[0])) 
		
		self.show()

	def openLiveStream(self):
		if self.kana.streamingStatus:
			for videos in self.kana.videoid:
				webbrowser.open("https://www.youtube.com/watch?v=" + videos)
		else:
			print("Not live")

	def resource_path(self,relative_path):
		if hasattr(sys, '_MEIPASS'):
			return os.path.join(sys._MEIPASS, relative_path)
		return os.path.join(os.path.abspath("."), relative_path)

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = KanaAlarm()
	sys.exit(app.exec_())
