# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, QWidget, QListView, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader


class Widget(QWidget):
    searchDir = "D:\workUni"
    fileList = []
    extractList = []
    def __init__(self):
        super(Widget, self).__init__()
        self.setWindowTitle("HelloWorld")
        self.load_ui()
        self.find = self.findChild(QPushButton, 'find')
        self.extract = self.findChild(QPushButton, 'extract')
        self.label = self.findChild(QLabel, 'label')
        self.list = self.findChild(QListView, 'listWidget')
        self.table = self.findChild(QTableWidget, 'tableWidget')
        self.find.clicked.connect(self.findFiles)
        self.extract.clicked.connect(self.extractFiles)
        self.table.cellClicked.connect(self.cell)

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
        for element in self.fileList:
            self.list.addItem(element)
        self.table.setColumnCount(1)
        self.table.setRowCount(len(self.fileList))
        for i, element in enumerate(self.fileList):
            self.table.setItem(i,0,QTableWidgetItem(element))
        self.label.setText(self.fileList.count)

    def extractFiles(self):
        for item in self.table.selectedItems():
            print (item.text())

    def cell(self, row, column):
        print(self.table.item(row,column).text())



if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
