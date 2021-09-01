# This Python file uses the following encoding: utf-8
import os
import time, threading

from pathlib import Path
import sys

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from zip import *


class Widget(QWidget):
    searchDir = "/home/miezekatzen/Downloads"
    extractDir = "/media/share/download/zeitung"
    fileList = []
    extractList = []

    def __init__(self):
        super(Widget, self).__init__()
        self.setWindowTitle("HelloWorld")
        self.load_ui()
        self.find = self.findChild(QPushButton, 'find')
        self.extract = self.findChild(QPushButton, 'extract')
        self.label = self.findChild(QLabel, 'label')
        self.table = self.findChild(QTableWidget, 'tableWidget')
        self.searchPath = self.findChild(QComboBox, 'searchPath')
        self.extractPath = self.findChild(QComboBox, 'extractPath')
        self.find.clicked.connect(self.findFiles)
        self.extract.clicked.connect(self.extractFiles)
        self.table.cellClicked.connect(self.cell)
        self.searchPath.currentTextChanged.connect(self.searchChange)
        self.extractPath.currentTextChanged.connect(self.extractChange)

        self.label.setText("Version 1.0")

        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def findFiles(self):
        for file in os.listdir(self.searchDir):
            if file.endswith(".zip"):
                qDebug(os.path.join(self.searchDir, file))
                self.fileList.append(os.path.join(self.searchDir, file))
        self.table.setColumnCount(1)
        self.table.setRowCount(len(self.fileList))
        for i, element in enumerate(self.fileList):
            self.table.setItem(i,0,QTableWidgetItem(element))

    def extractFiles(self):
        for item in self.table.selectedItems():
            print (item.text())

    def cell(self, row, column):
        self.label.setText("Working")
        currentZip = zip(self.table.item(row,column).text(), self.extractDir)
        extractPassed = currentZip.extract()
        self.label.setText(extractPassed)
        threading.Timer(1, self.removeLabel).start()

    def removeLabel(self):
        self.label.setText('')

    def searchChange(self, strDir):
        self.searchDir = strDir

    def extractChange(self, strDir):
        self.extractDir = strDir



if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
