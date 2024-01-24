# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerlwjCWj.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_P2PChat(object):
    def setupUi(self, P2PChat):
        if not P2PChat.objectName():
            P2PChat.setObjectName(u"P2PChat")
        P2PChat.resize(1026, 656)
        self.centralwidget = QWidget(P2PChat)
        self.centralwidget.setObjectName(u"centralwidget")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(230, 449, 621, 51))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setAutoFillBackground(False)
        self.listView = QListView(self.centralwidget)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(0, 10, 221, 491))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(860, 460, 101, 31))
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(230, 10, 741, 431))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 739, 429))
        self.textEdit_2 = QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(0, 0, 741, 431))
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.textEdit_2.sizePolicy().hasHeightForWidth())
        self.textEdit_2.setSizePolicy(sizePolicy1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        P2PChat.setCentralWidget(self.centralwidget)

        self.retranslateUi(P2PChat)

        QMetaObject.connectSlotsByName(P2PChat)
    # setupUi

    def retranslateUi(self, P2PChat):
        P2PChat.setWindowTitle(QCoreApplication.translate("P2PChat", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("P2PChat", u"Send Meassge", None))
    # retranslateUi

