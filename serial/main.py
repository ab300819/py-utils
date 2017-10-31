#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import QApplication
from MyCOM import MainWidget

__author__ = "Apache"
__version__ = "0.1"
__email__ = "hqwemail@163.com"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Plastique")
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())