# This Python file uses the following encoding: utf-8
import zipfile
from PySide2.QtCore import *

class zip (QObject):

    finished = Signal()

    def __init__(self, searchDir, extractDir):
        self.searchDir = searchDir
        self.extractDir = extractDir

    def run(self):
        r = zipfile.ZipFile(self.searchDir)
        r.extractall(self.extractDir)
        r.close()
        self.finished.emit()

