from logging import FileHandler,INFO,WARNING,ERROR

class InfoFileHandler(FileHandler):
    def __init__(self,filename,mode='a',encoding=None,delay=False):
        FileHandler.__init__(self,filename,mode,encoding,delay)

    def emit(self, record):
        if not record.levelno == INFO:
            return
        FileHandler.emit(self,record)

class WarningFileHandler(FileHandler):
    def __init__(self,filename,mode='a',encoding=None,delay=False):
        FileHandler.__init__(self,filename,mode,encoding,delay)

    def emit(self, record):
        if not record.levelno == WARNING:
            return
        FileHandler.emit(self,record)

class ErrorFileHandler(FileHandler):
    def __init__(self,filename,mode='a',encoding=None,delay=False):
        FileHandler.__init__(self,filename,mode,encoding,delay)

    def emit(self, record):
        if not record.levelno == ERROR:
            return
        FileHandler.emit(self,record)