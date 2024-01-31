from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import os
import json
import sys
import socket
from pathlib import Path
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QFileDialog

sys.path.append('./')
from utils.helpers import (
    get_self_ip
)

from utils.types import HeaderCode

SERVER_IP = ""
SERVER_ADDR = ()
CLIENT_IP = get_self_ip()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1090, 761)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(10, 0, 10, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Buttons = QtWidgets.QHBoxLayout()
        self.Buttons.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.Buttons.setSpacing(6)
        self.Buttons.setObjectName("Buttons")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.Buttons.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Buttons.addItem(spacerItem)
        self.btnGlobalSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnGlobalSearch.setObjectName("btnGlobalSearch")
        self.Buttons.addWidget(self.btnGlobalSearch)
        self.btnAddFiles = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddFiles.setObjectName("btnAddFiles")
        self.Buttons.addWidget(self.btnAddFiles)
        self.btnSettings = QtWidgets.QPushButton(self.centralwidget)
        self.btnSettings.setObjectName("btnSettings")
        self.Buttons.addWidget(self.btnSettings)
        self.verticalLayout.addLayout(self.Buttons)
        self.Content = QtWidgets.QHBoxLayout()
        self.Content.setObjectName("Content")
        self.FilesAndUsers = QtWidgets.QVBoxLayout()
        self.FilesAndUsers.setSpacing(8)
        self.FilesAndUsers.setObjectName("FilesAndUsers")
        self.usersLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.usersLabel.setFont(font)
        self.usersLabel.setObjectName("usersLabel")
        self.FilesAndUsers.addWidget(self.usersLabel)
        self.usersList = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usersList.sizePolicy().hasHeightForWidth())
        self.usersList.setSizePolicy(sizePolicy)
        self.usersList.setObjectName("usersList")
        item = QtWidgets.QListWidgetItem()
        self.usersList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.usersList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.usersList.addItem(item)
        self.FilesAndUsers.addWidget(self.usersList)
        self.filesLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.filesLabel.setFont(font)
        self.filesLabel.setObjectName("filesLabel")
        self.FilesAndUsers.addWidget(self.filesLabel)
        self.filesTree = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filesTree.sizePolicy().hasHeightForWidth())
        self.filesTree.setSizePolicy(sizePolicy)
        self.filesTree.setObjectName("filesTree")
        item_0 = QtWidgets.QTreeWidgetItem(self.filesTree)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.filesTree)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.filesTree)
        item_0 = QtWidgets.QTreeWidgetItem(self.filesTree)
        item_0 = QtWidgets.QTreeWidgetItem(self.filesTree)
        self.filesTree.header().setVisible(True)
        self.FilesAndUsers.addWidget(self.filesTree)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setEnabled(True)
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setEnabled(True)
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.FilesAndUsers.addLayout(self.horizontalLayout_2)
        self.Content.addLayout(self.FilesAndUsers)
        self.Chat = QtWidgets.QVBoxLayout()
        self.Chat.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.Chat.setObjectName("Chat")
        self.chatLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.chatLabel.setFont(font)
        self.chatLabel.setObjectName("chatLabel")
        self.Chat.addWidget(self.chatLabel)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.textEdit.setObjectName("textEdit")
        self.Chat.addWidget(self.textEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 80))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_6.addWidget(self.pushButton_3)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_6.addWidget(self.pushButton_6)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.Chat.addLayout(self.horizontalLayout)
        self.Chat.setStretch(2, 1)
        self.Content.addLayout(self.Chat)
        self.Content.setStretch(0, 1)
        self.Content.setStretch(1, 2)
        self.verticalLayout.addLayout(self.Content)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 150))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1025, 344))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_6 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_6.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_10 = QtWidgets.QLabel(self.widget_6)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_8.addWidget(self.label_10)
        self.progressBar_6 = QtWidgets.QProgressBar(self.widget_6)
        self.progressBar_6.setProperty("value", 24)
        self.progressBar_6.setObjectName("progressBar_6")
        self.horizontalLayout_8.addWidget(self.progressBar_6)
        self.verticalLayout_5.addWidget(self.widget_6)
        self.widget_3 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.widget_3)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.progressBar_3 = QtWidgets.QProgressBar(self.widget_3)
        self.progressBar_3.setProperty("value", 24)
        self.progressBar_3.setObjectName("progressBar_3")
        self.horizontalLayout_5.addWidget(self.progressBar_3)
        self.verticalLayout_5.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_4.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.widget_4)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_6.addWidget(self.label_8)
        self.progressBar_4 = QtWidgets.QProgressBar(self.widget_4)
        self.progressBar_4.setProperty("value", 24)
        self.progressBar_4.setObjectName("progressBar_4")
        self.horizontalLayout_6.addWidget(self.progressBar_4)
        self.verticalLayout_5.addWidget(self.widget_4)
        self.widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 40))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.progressBar = QtWidgets.QProgressBar(self.widget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_3.addWidget(self.progressBar)
        self.verticalLayout_5.addWidget(self.widget, 0, QtCore.Qt.AlignTop)
        self.widget_5 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_5.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_9 = QtWidgets.QLabel(self.widget_5)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_7.addWidget(self.label_9)
        self.progressBar_5 = QtWidgets.QProgressBar(self.widget_5)
        self.progressBar_5.setProperty("value", 24)
        self.progressBar_5.setObjectName("progressBar_5")
        self.horizontalLayout_7.addWidget(self.progressBar_5)
        self.verticalLayout_5.addWidget(self.widget_5)
        self.widget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.widget_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.progressBar_2 = QtWidgets.QProgressBar(self.widget_2)
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setObjectName("progressBar_2")
        self.horizontalLayout_4.addWidget(self.progressBar_2)
        self.verticalLayout_5.addWidget(self.widget_2)
        self.widget_7 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        self.widget_7.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_7.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_11 = QtWidgets.QLabel(self.widget_7)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_9.addWidget(self.label_11)
        self.progressBar_7 = QtWidgets.QProgressBar(self.widget_7)
        self.progressBar_7.setProperty("value", 24)
        self.progressBar_7.setObjectName("progressBar_7")
        self.horizontalLayout_9.addWidget(self.progressBar_7)
        self.verticalLayout_5.addWidget(self.widget_7, 0, QtCore.Qt.AlignTop)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        spacerItem2 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.init_views()
        self.on_click_listeners()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Echo"))
        self.label_3.setText(_translate("MainWindow", "Echo / john_doe_"))
        self.btnGlobalSearch.setText(_translate("MainWindow", "Gobal Search"))
        self.btnAddFiles.setText(_translate("MainWindow", "Add Files"))
        self.btnSettings.setText(_translate("MainWindow", "Settings"))
        self.usersLabel.setText(_translate("MainWindow", "Users"))
        __sortingEnabled = self.usersList.isSortingEnabled()
        self.usersList.setSortingEnabled(False)
        item = self.usersList.item(0)
        item.setText(_translate("MainWindow", "Aviiiii"))
        item = self.usersList.item(1)
        item.setText(_translate("MainWindow", "koi bhi ensaan"))
        item = self.usersList.item(2)
        item.setText(_translate("MainWindow", "Yuvraj"))
        self.usersList.setSortingEnabled(__sortingEnabled)
        self.filesLabel.setText(_translate("MainWindow", "Browse Files"))
        self.filesTree.headerItem().setText(0, _translate("MainWindow", "RichardRoe12"))
        __sortingEnabled = self.filesTree.isSortingEnabled()
        self.filesTree.setSortingEnabled(False)
        self.filesTree.topLevelItem(0).setText(0, _translate("MainWindow", "Movies/"))
        self.filesTree.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "The Matrix.mov"))
        self.filesTree.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "Forrest Gump.mp4"))
        self.filesTree.topLevelItem(0).child(2).setText(0, _translate("MainWindow", "Django.mp4"))
        self.filesTree.topLevelItem(1).setText(0, _translate("MainWindow", "Games/"))
        self.filesTree.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "NFS/"))
        self.filesTree.topLevelItem(1).child(1).setText(0, _translate("MainWindow", "nfsmostwanted.zip"))
        self.filesTree.topLevelItem(1).child(2).setText(0, _translate("MainWindow", "TLauncher.zip"))
        self.filesTree.topLevelItem(1).child(3).setText(0, _translate("MainWindow", "GTA-V.iso"))
        self.filesTree.topLevelItem(2).setText(0, _translate("MainWindow", "photoshop.iso"))
        self.filesTree.topLevelItem(3).setText(0, _translate("MainWindow", "msoffice.zip"))
        self.filesTree.topLevelItem(4).setText(0, _translate("MainWindow", "Study Material/"))
        self.filesTree.setSortingEnabled(__sortingEnabled)
        self.label_4.setText(_translate("MainWindow", "Selected File/Folder: msoffice.zip"))
        self.pushButton_5.setText(_translate("MainWindow", "Info"))
        self.pushButton_4.setText(_translate("MainWindow", "Download"))
        self.chatLabel.setText(_translate("MainWindow", "Chat with Aviii"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:6.6pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:600; color:#e5a50a;\">12:03</span><span style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:600;\"> RichardRoe12: </span><span style=\" font-family:\'Noto Sans\'; font-size:10pt;\">Hello</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:600; color:#1a5fb4;\">12:03</span><span style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:600;\"> You: </span><span style=\" font-family:\'Noto Sans\'; font-size:10pt;\">Hii</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:600; color:#e5a50a;\">12:03</span><span style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:600;\"> RichardRoe12: </span><span style=\" font-family:\'Noto Sans\'; font-size:10pt;\">Got any games?</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:600; color:#1a5fb4;\">12:03</span><span style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:600;\"> You: </span><span style=\" font-family:\'Noto Sans\'; font-size:10pt;\">Probably</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:600; color:#1a5fb4;\">12:03</span><span style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:600;\"> You: </span><span style=\" font-family:\'Noto Sans\'; font-size:10pt;\">Wait ill upload something...</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.plainTextEdit.setPlaceholderText(_translate("MainWindow", "Enter message"))
        self.pushButton_3.setText(_translate("MainWindow", "Send Message"))
        self.pushButton_6.setText(_translate("MainWindow", "Send File"))
        self.label_12.setText(_translate("MainWindow", "Downloading:"))
        self.label_10.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "TextLabel"))
        self.label_8.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "TextLabel"))
        self.label_9.setText(_translate("MainWindow", "TextLabel"))
        self.label_6.setText(_translate("MainWindow", "TextLabel"))
        self.label_11.setText(_translate("MainWindow", "TextLabel"))
    
    def list_files_and_empty_folders(self, folder_path):
        file_list = []

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(str(file_path))
            
            for folder in dirs:
                folder_path = os.path.join(root, folder)
                file_list.append(str(folder_path))
        return file_list

    def to_json(self):
        list = self.list_files_and_empty_folders('./public')
        tree = {}
        for path in list:                
            node = tree                   
            for level in path.split('\\'): 
                if level:                 
                    node = node.setdefault(level, dict())
        # with open('output.json', 'w') as json_file:
        #     json.dump(tree, json_file, indent=2)
        return tree
        
    def thread(self, chat_socket): 
        t1 = threading.Thread(target=self.receive_chat, args=(chat_socket,))
        t1.start()

    def receive_chat(self,client_socket):
        while True:
            try:
                response = client_socket.recv(1024).decode('utf-8')
                response = response.split('@')

                if response[0] == str(HeaderCode.MESSAGE):
                    message = response[1]
                    self.textEdit.append("Sender: " + message)
                
                elif response[0] == str(HeaderCode.FILE_SHARE):
                    global host
                    port_file_to_connect = int(response[1])

                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                    sock.connect((host, port_file_to_connect)) 

                    download_path = './download'

                    if not os.path.exists(download_path):
                        os.makedirs(download_path)
                    
                    self.receive_file(sock, download_path)


            except Exception as e:
                print(f"Error receiving chat message: {e}")
            
    def send_request(self, client_socket, request, message=None):
        try:
            if(request == HeaderCode.MESSAGE):
                message = str(request) + '@' + self.plainTextEdit.toPlainText()
                client_socket.send(message.encode('utf-8'))
                self.textEdit.append("You: " + self.plainTextEdit.toPlainText())
                self.plainTextEdit.clear()

            elif(request == HeaderCode.FILE_SHARE):
                message = str(request) + '@' + str(message)
                client_socket.send(message.encode('utf-8'))

                
        except Exception as e:
            print(f"Error sending request: {e}")

    def receive_file(self, client_socket, download_path):
        try:
            file_name = client_socket.recv(1024).decode('utf-8')
            file_path = os.path.join(download_path, file_name)
            with open(file_path, 'wb') as file:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)
            print(f"File received and saved at: {file_path}")
        except Exception as e:
            print(f"Error receiving file: {e}")

    def on_send_file_clicked(self):
        #Open Qfile dialog to select file/files
        global port_file
        file_paths = QFileDialog.getOpenFileNames(
            None, 
            "Select Files",
            str(Path.home()))

        print('file_path :',file_paths)

        for file_path in file_paths[0]:
            file_name = os.path.basename(file_path)
            global request_socket
            self.send_request(request_socket, HeaderCode.FILE_SHARE, port_file)
            
        

    def send_file(self, file_path, port_file):
        global host

        file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file_socket.bind((host, port_file))
        file_socket.listen()

        print(f"File server listening on {host}:{port_file}")

        file_client, file_addr = file_socket.accept()
        print(f"File connection established with {file_addr}")
        try:
            file_name = os.path.basename(file_path)
            file_client.send(file_name.encode('utf-8'))
            print("Sending file...")
            with open(file_path, 'rb') as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    file_client.send(data)
            print("File sent")
        except Exception as e:
            print(f"Error sending file: {e}")
            
    def add_data_to_tree(self, tree_widget, data):
        def add_items(parent_item, items):
            for key, value in items.items():
                if isinstance(value, dict):
                    child_item = QTreeWidgetItem()
                    child_item.setText(0, key)
                    parent_item.addChild(child_item)
                    add_items(child_item, value)
                else:
                    child_item = QTreeWidgetItem(parent_item)
                    child_item.setText(0, value)

        tree_widget.clear()

        for key, value in data.items():
            top_level_item = QTreeWidgetItem(tree_widget)
            top_level_item.setText(0, key)
            add_items(top_level_item, value)

    def on_tree_item_clicked(self, item, column):
        print(item.text(column))
    
    def on_list_widget_item_clicked(self, item):
        print(item.text())
      

    def main(self):
        global host
        global request_socket
        host = '192.168.137.1'
        port_chat = 5555
        port_file = 5556
        
        receiver = ('192.168.137.1', port_chat)

        chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        client = 0
        
        if (client):
            chat_socket.connect(receiver)
            print("Connected to chat server")

            request_socket = chat_socket

        else:
            chat_socket.bind((host, port_chat))
            chat_socket.listen()
        
            print(f"Chat server listening on {host}:{port_chat}")
            request_socket, chat_addr = chat_socket.accept()
            print("Connected to chat server")
        
        self.pushButton_3.clicked.connect(lambda: self.send_request(request_socket, HeaderCode.MESSAGE))
        self.btnSettings.clicked.connect(lambda: self.thread(request_socket))
    
    def init_views(self):
        self.main()

        # Clear chat field
        self.textEdit.clear()

        # Add data to tree widget
        self.add_data_to_tree(self.filesTree, self.to_json())
    
    def on_click_listeners(self):
        # on tree widget item clicked
        self.filesTree.itemClicked.connect(self.on_tree_item_clicked)

        # on send message button clicked
        self.pushButton_6.clicked.connect(self.on_send_file_clicked)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())