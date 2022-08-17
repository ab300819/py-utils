#-*- coding: utf-8 -*-
from time import ctime
from PyQt4.QtGui import QKeySequence, QIcon, QPixmap
from PyQt4.QtCore import Qt
from MyCOM_Ui import Ui_Form as MyCOM_UIForm
import Util

class MyCOM_UiHandler(MyCOM_UIForm):
    def __init__(self, parent=None):
        MyCOM_UIForm.__init__(self)
    
    def setupWidget(self, wobj):
        wobj.setWindowIcon(QIcon(QPixmap(":/icon/icons/logo.png")))
        self.sendButton.setShortcut(QKeySequence(Qt.Key_Return + Qt.CTRL))
        
    def getPortSettings(self):
        settings = {
            "port": None, "baund": 9600, "bytesize": 8,
            "parity": "no", "stopbits": 1, "timeout": 1}
        fieldmap = ("port", "baund", "bytesize", "parity", "stopbits")
        settings_line = self.setComboBox.currentText().toUtf8().data()
        fields = settings_line.split(':')
        for i in xrange(len(fields)):
            settings[fieldmap[i]] = fields[i]

        return settings
    
    def getDataAndType(self):
        return self.sendTextEdit.toPlainText().toUtf8().data(), self.radioButton.isChecked() and "ascii" or "hex"
        
    def onPortOpened(self):
        self.openButton.setText(u"关闭")
        self.tipsLabel.setText("++Port is open:)")
        
    def onPortOpening(self):
        self.tipsLabel.setText("Try to open port, please wait...")
    
    def onPortClosed(self):
        self.openButton.setText(u"打开")
        self.tipsLabel.setText("--Port is closed:-")
    
    def onSendData(self, data=None, _type="ascii"):
        if not data: data = self.sendTextEdit.toPlainText()
        if _type == "hex":
            data = ''.join(data.split())
            data = ' '.join([data[i:i+2] for i in xrange(0, len(data), 2)]).upper()
        else:
            data = data.replace('\n', '<br/>')
        self.chatTextBrowser.append('<b>Send</b> @%s<br/><font color="white">%s</font><br/><br/>'
                                    % (ctime(), data))
        self.sendTextEdit.clear()
        bytes = _type == "ascii" and len(data) or len(data) / 2
        self.sendLcdNumber.display(self.sendLcdNumber.intValue() + bytes)
    
    def onRecvData(self, data):
        bytes = len(data)
        if not self.radioButton.isChecked():
            data = Util.toVisualHex(data)
        else:
            data = data.replace('\n', '<br/>')
        self.chatTextBrowser.append('<b>Recv</b> @%s<br/><font color="yellow">%s</font><br/><br/>'
                                    % (ctime(), data))
        self.recvLcdNumber.display(self.recvLcdNumber.intValue() + bytes)
    
    def clearLcdNumber(self):
        self.sendLcdNumber.display(0)
        self.recvLcdNumber.display(0)
    
    def clearHistory(self):
        self.chatTextBrowser.clear()