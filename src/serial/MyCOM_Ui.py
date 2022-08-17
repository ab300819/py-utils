# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyCOM.ui'
#
# Created: Sun Nov 11 13:12:57 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(643, 489)
        Form.setStyleSheet(_fromUtf8("font: 9pt \"Lucida Console\";"))
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.tipsLabel = QtGui.QLabel(Form)
        self.tipsLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.tipsLabel.setObjectName(_fromUtf8("tipsLabel"))
        self.horizontalLayout_3.addWidget(self.tipsLabel)
        self.setComboBox = QtGui.QComboBox(Form)
        self.setComboBox.setEditable(True)
        self.setComboBox.setObjectName(_fromUtf8("setComboBox"))
        self.setComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.setComboBox)
        self.openButton = QtGui.QPushButton(Form)
        self.openButton.setMaximumSize(QtCore.QSize(75, 16777215))
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.horizontalLayout_3.addWidget(self.openButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.chatTextBrowser = QtGui.QTextBrowser(self.splitter)
        self.chatTextBrowser.setStyleSheet(_fromUtf8("background-color: rgb(36, 36, 36);\n"
"color: rgb(12, 190, 255);"))
        self.chatTextBrowser.setObjectName(_fromUtf8("chatTextBrowser"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.radioButton = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.horizontalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.horizontalLayout_2.addWidget(self.radioButton_2)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(488, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.clearHistoryButton = QtGui.QPushButton(self.layoutWidget)
        self.clearHistoryButton.setObjectName(_fromUtf8("clearHistoryButton"))
        self.horizontalLayout_4.addWidget(self.clearHistoryButton)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.sendTextEdit = QtGui.QTextEdit(self.layoutWidget)
        self.sendTextEdit.setStyleSheet(_fromUtf8("background-color: rgb(36, 36, 36);\n"
"color: rgb(12, 190, 255);"))
        self.sendTextEdit.setObjectName(_fromUtf8("sendTextEdit"))
        self.gridLayout.addWidget(self.sendTextEdit, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.splitter, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.recvLcdNumber = QtGui.QLCDNumber(Form)
        self.recvLcdNumber.setObjectName(_fromUtf8("recvLcdNumber"))
        self.horizontalLayout.addWidget(self.recvLcdNumber)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.sendLcdNumber = QtGui.QLCDNumber(Form)
        self.sendLcdNumber.setObjectName(_fromUtf8("sendLcdNumber"))
        self.horizontalLayout.addWidget(self.sendLcdNumber)
        self.clearLcdButton = QtGui.QPushButton(Form)
        self.clearLcdButton.setObjectName(_fromUtf8("clearLcdButton"))
        self.horizontalLayout.addWidget(self.clearLcdButton)
        spacerItem1 = QtGui.QSpacerItem(148, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.resetArduinoButton = QtGui.QPushButton(Form)
        self.resetArduinoButton.setObjectName(_fromUtf8("resetArduinoButton"))
        self.horizontalLayout.addWidget(self.resetArduinoButton)
        self.sendButton = QtGui.QPushButton(Form)
        self.sendButton.setObjectName(_fromUtf8("sendButton"))
        self.horizontalLayout.addWidget(self.sendButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "MyCOM", None, QtGui.QApplication.UnicodeUTF8))
        self.tipsLabel.setText(QtGui.QApplication.translate("Form", "Welcome to MyCOM | Create by Apache", None, QtGui.QApplication.UnicodeUTF8))
        self.setComboBox.setItemText(0, QtGui.QApplication.translate("Form", "COM3:9600:8:N:1", None, QtGui.QApplication.UnicodeUTF8))
        self.openButton.setText(QtGui.QApplication.translate("Form", "打开", None, QtGui.QApplication.UnicodeUTF8))
        self.chatTextBrowser.setHtml(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Console\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("Form", "ASCII", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setText(QtGui.QApplication.translate("Form", "HEX", None, QtGui.QApplication.UnicodeUTF8))
        self.clearHistoryButton.setText(QtGui.QApplication.translate("Form", "清空历史", None, QtGui.QApplication.UnicodeUTF8))
        self.sendTextEdit.setHtml(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Console\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Recv", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Send", None, QtGui.QApplication.UnicodeUTF8))
        self.clearLcdButton.setText(QtGui.QApplication.translate("Form", "清零", None, QtGui.QApplication.UnicodeUTF8))
        self.resetArduinoButton.setText(QtGui.QApplication.translate("Form", "ResetArduino", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("Form", "发送", None, QtGui.QApplication.UnicodeUTF8))

