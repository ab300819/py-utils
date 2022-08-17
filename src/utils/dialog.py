#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QApplication, QPushButton


@Slot()
def say_hello():
    print('Button clicked, Hello!')


app = QApplication(sys.argv)
button = QPushButton('Click Me')
button.clicked.connect(say_hello)
button.show()
app.exec_()
