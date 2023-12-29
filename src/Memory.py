import random

class Memory:
    def __init__(self, size, directory=None, DirectoryController=None):
        Memory_contents = {}
        for i in range(size):
            Memory_contents[i] = 0
        self.content = Memory_contents
        self.directory = directory
        self.DirectoryController = DirectoryController

    def connect(self, directory, DirectoryController):
        self.directory = directory
        self.DirectoryController = DirectoryController
