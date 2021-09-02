# This Python file uses the following encoding: utf-8
import rarfile
from PySide2.QtCore import *

class rar:
    def __init__(self, searchDir, extractDir):
        self.searchDir = searchDir
        self.extractDir = extractDir
        qDebug(self.searchDir)
        qDebug(self.extractDir)

    def extract(self):
        r = rarfile.RarFile(self.searchDir)
        rInfo = r.infolist()
        for items in rInfo:
            print(items.filename)
        r.extractall(self.extractDir)
        r.close()
        return ("Passed")

