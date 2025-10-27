#-*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from MyCOM_UiHandler import MyCOM_UiHandler
from MySerial import MySerial
from Icons import *
import Util

class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        
        self.ui = MyCOM_UiHandler()
        self.flags = {"__isopen__": False, "__datatype__": "ascii"}
        
        self.ui.setupUi(self)
        self.ui.setupWidget(self)
        self.__setupSignal()
    
    def closeEvent(self, e):
        if self.flags["__isopen__"]:
            self.serial.terminate()
        e.accept()
        
    def __setupSignal(self):
        self.ui.openButton.clicked.connect(self.__onOpenPort)
        self.ui.sendButton.clicked.connect(self.__onSendData)        
        self.ui.resetArduinoButton.clicked.connect(self.__onResetArduino)        
        self.ui.clearHistoryButton.clicked.connect(self.ui.clearHistory)        
        self.ui.clearLcdButton.clicked.connect(self.ui.clearLcdNumber)        

    def __openPort(self, settings=None):
        if not settings:
            settings = self.ui.getPortSettings()
            ret, msg = Util.formatPortSettins(settings)
            if not ret:
                return False, msg
                
        if not settings["port"]:
            return False, u"错误的串口号"
            
        self.serial = MySerial()
        self.connect(self.serial.qtobj, QtCore.SIGNAL("NewData"), self.ui.onRecvData)
        ret, msg = self.serial.open(settings)
        
        return ret, msg
        
    def __closePort(self):
        self.serial.terminate()
        self.ui.onPortClosed()
        self.flags["__isopen__"] = False
        
    def __onOpenPort(self):
        if self.flags["__isopen__"]:
            return self.__closePort()
            
        self.ui.onPortOpening()
        ret, msg = self.__openPort()
        if not ret:
            QtGui.QMessageBox.critical(self, "Error", msg)
        else:
            self.flags["__isopen__"] = True
            self.serial.start()
            self.ui.onPortOpened()
    
    def __onSendData(self):
        if not self.flags["__isopen__"]:
            QtGui.QMessageBox.information(self, "Tips", u"请先打开串口")
            return
        data, _type = self.ui.getDataAndType()
        ret, msg = Util.checkData(data, _type)
        if not ret:
            QtGui.QMessageBox.critical(self, "Error", u"%s" % msg)
            return
        
        self.ui.onSendData(data, _type)
        if _type == "hex":
            data = Util.toHex(''.join(data.split()))
        self.serial.send(data, _type)
    
    def __onResetArduino(self):
        if not self.flags["__isopen__"]:
            QtGui.QMessageBox.information(self, "Tips", u"请先打开串口")
            return
            
        self.serial.resetArduino()
        QtGui.QMessageBox.information(self, "Tips", u"Reset Arduino完成")