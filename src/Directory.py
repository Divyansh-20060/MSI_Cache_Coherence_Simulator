class Directory:
    def __init__(self, size, DirectoryController=None, memory=None):
        Directory_contents = {}
        for i in range(size):
            sharer_list = [0, 0, 0, 0]
            x = {"state": "invalid", "owner": -1, "sharer_list": sharer_list}
            Directory_contents[i] = x

        self.content = Directory_contents
        self.DirectoryController = DirectoryController
        self.memory = memory

    def connect(self, DirectoryController, memory):
        self.DirectoryController = DirectoryController
        self.memory = memory
