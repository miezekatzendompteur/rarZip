# This Python file uses the following encoding: utf-8
import zipfile

class zip:
    def __init__(self, searchDir, extractDir):
        self.searchDir = searchDir
        self.extractDir = extractDir
        pass
    def extract(self):
        r = zipfile.ZipFile(self.searchDir)
        #r.extractall(self.extractDir)
        #r.close()
        return ("Passed")

