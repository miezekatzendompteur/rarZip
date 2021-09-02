# This Python file uses the following encoding: utf-8
import os
import time

from pathlib import Path
import sys

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from zip import zip
from rar import rar


class Widget(QWidget):
    #searchDir = "/home/miezekatzen/Downloads"
    #extractDir = "/media/share/download/zeitung"

    defaultSearch = r"d:\download"
    defaultExtract = r"d:\extract"

    searchDir = ""
    extractDir = ""

    extractTypeZip = True
    extractTypeRar = False

    fileList = []
    extractList = []

    def __init__(self):
        super(Widget, self).__init__()
        self.setWindowTitle("HelloWorld")
        self.load_ui()
        self.find = self.findChild(QPushButton, 'find')

        self.browsSearch = self.findChild(QPushButton, 'browsSearch')
        self.browsExtract = self.findChild(QPushButton, 'browsExtract')
        self.label = self.findChild(QLabel, 'label')
        self.table = self.findChild(QTableWidget, 'tableWidget')
        self.searchPath = self.findChild(QComboBox, 'searchPath')
        self.extractPath = self.findChild(QComboBox, 'extractPath')
        self.zipButton = self.findChild(QRadioButton, 'zip')
        self.rarButton = self.findChild(QRadioButton, 'rar')

        self.searchDir = os.getcwd()
        self.extractDir = os.getcwd()

        self.searchPath.insertItem(0, self.searchDir)
        self.searchPath.setCurrentIndex(0)

        self.extractPath.insertItem(0, self.extractDir)
        self.extractPath.setCurrentIndex(0)

        self.zipButton.setChecked(True)
        self.rarButton.setChecked(False)


        self.zipButton.clicked.connect(self.changeZip)
        self.rarButton.clicked.connect(self.changeRar)
        self.browsSearch.clicked.connect(self.browsSearchFunction)
        self.browsExtract.clicked.connect(self.browsExtractFunction)
        self.find.clicked.connect(self.findFiles)

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
        self.fileList.clear()
        self.table.setRowCount(0)

        if self.extractTypeZip == False and self.extractTypeRar == True:
            for file in os.listdir(self.searchDir):
                if file.endswith(".rar"):
                    qDebug(os.path.join(self.searchDir, file))
                    self.fileList.append(os.path.join(self.searchDir, file))
        elif self.extractTypeZip == True and self.extractTypeRar == False:
            for file in os.listdir(self.searchDir):
                if file.endswith(".zip"):
                    qDebug(os.path.join(self.searchDir, file))
                    self.fileList.append(os.path.join(self.searchDir, file))
        self.table.setColumnCount(1)
        self.table.setRowCount(len(self.fileList))
        for i, element in enumerate(self.fileList):
            self.table.setItem(i,0,QTableWidgetItem(element))

    def cell(self, row, column):
        self.label.setText("Working")

        if self.extractTypeZip == False and self.extractTypeRar == True:
            self.thread = QThread()
            self.currentRar = rar(self.table.item(row,column).text(), self.extractDir)
            self.currentRar.moveToThread(self.thread)

            self.thread.started.connect(self.currentRar.run)
            self.currentRar.finished.connect(self.thread.quit)

            self.thread.start()

            extractPassed = currentRar.extract()
        elif self.extractTypeZip == True and self.extractTypeRar == False:

            self.thread = QThread()
            self.currentZip = zip(self.table.item(row,column).text(), self.extractDir)
            self.currentZip.moveToThread(self.thread)

            self.thread.started.connect(self.currentZip.run)
            self.currentZip.finished.connect(self.thread.quit)

            self.thread.start()

        self.label.setText(extractPassed)
        threading.Timer(1, self.removeLabel).start()

    def removeLabel(self):
        self.label.setText('')

    def searchChange(self, strDir):
        self.searchDir = strDir
        print(self.searchDir)

    def extractChange(self, strDir):
        self.extractDir = strDir
        print(self.extractDir)

    def browsSearchFunction(self):
        addDir = QFileDialog.getExistingDirectory(self, "Open Directory", self.defaultSearch, QFileDialog.ShowDirsOnly)
        lastIndex = self.searchPath.count() - 1
        self.searchPath.insertItem(lastIndex + 1, addDir)
        self.searchPath.setCurrentIndex(lastIndex + 1)

    def browsExtractFunction(self):
        addDir = QFileDialog.getExistingDirectory(self, "Open Directory", self.defaultExtract, QFileDialog.ShowDirsOnly)
        lastIndex = self.searchPath.count() - 1
        self.searchPath.insertItem(lastIndex + 1, addDir)
        self.searchPath.setCurrentIndex(lastIndex + 1)

    def changeRar(self):
        self.extractTypeZip = False
        self.extractTypeRar = True


    def changeZip(self):
        self.extractTypeZip = True
        self.extractTypeRar = False


if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
