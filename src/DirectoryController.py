class DirectoryController:
    def __init__(self, directory=None, memory=None, CacheController_list=None):
        self.directory = directory
        self.memory = memory
        self.CacheController_list = CacheController_list
        self.NumDirectoryUpdates = 0

    def write(self, address, data):
        self.memory.content[address] = data

    def data(self, cc, data, address, state):
        self.directory.content[address]["state"] = state
        self.directory.content[address]["owner"] = -1
        self.directory.content[address]["sharer_list"][cc.id] = 1

    def connect(self, directory , memory , CacheController_list):
        self.directory = directory
        self.memory = memory
        self.CacheController_list = CacheController_list

    def getS(self, cc , address):
        f = open ("Log_output\SystemLogs.txt", "a")

        state = self.directory.content[address]["state"]
        self.NumDirectoryUpdates += 1 ## Updating Directory
        if state == "invalid" or state == "shared": ## only Invalid is Correct In shared fwd-getS
        # if state == "invalid": ## only Invalid is Correct In shared fwd-getS
            
            self.directory.content[address]["state"] = "shared"
            self.directory.content[address]["owner"] = -1
            self.directory.content[address]["sharer_list"][cc.id] = 1
            # call the CacheController's data function
            data = self.memory.content[address]
            f.write(", DirectoryController sent "+ str(data) +"with State Shared to Cache" + str(cc.id+1) + " for address " + str(address))
            f.close()
            cc.data(address, data, "shared")

        if state == "modified" or state == "owned":
            # self.directory[address]["state"] = "shared"
            
            self.directory.content[address]["sharer_list"][cc.id] = 1
            owner = self.CacheController_list[self.directory.content[address]["owner"]]
            self.directory.content[address]["state"] = "owned"
            self.directory.content[address]["owner"] = cc.id
            f.write(", DirectoryController transact Fwd-GetShared (Fwd-getS) for address " + str(address) + "to Cache" + str(owner.id+1))
            f.close()
            owner.fwd_getS(cc, address)



    def getM(self, cc, address):

        state = self.directory.content[address]["state"]
        self.NumDirectoryUpdates += 1 ## Updating Directory
        if state == "invalid":
            self.directory.content[address]["owner"] = cc.id
            self.directory.content[address]["state"] = "modified"
            data = self.directory.memory.content[address]
            f = open ("Log_output\SystemLogs.txt", "a")
            f.write(", DirectoryController sent "+ str(data) +"with State Modified to Cache" + str(cc.id+1) + " for address " + str(address))
            f.close()
            cc.data(address, data, "modified")
        if state == "modified":
            owner = self.CacheController_list[self.directory.content[address]["owner"]]
            f = open ("Log_output\SystemLogs.txt", "a")
            f.write(", DirectoryController transact Fwd-GetModified (Fwd-getM) for address " + str(address) + "to Cache" + str(owner.id+1))
            f.close()
            owner.fwd_getM(cc, address)
            self.directory.content[address]["owner"] = cc.id

        if state == "shared":
            self.directory.content[address]["state"] = "modified"
            self.directory.content[address]["owner"] = cc.id
            f = open ("Log_output\SystemLogs.txt", "a")
            for i in range(4):
                if self.directory.content[address]["sharer_list"][i] == 1:
                    f.write(", DirectoryController Invalidated address " + str(address) + " from Cache" + str(self.CacheController_list[i].id+1))
                    self.CacheController_list[i].dir_inv(address)
                    self.directory.content[address]["sharer_list"][i] = 0
            data = self.directory.memory.content[address]
            f.write(", DirectoryController sent "+ str(data) +"with State Modified to Cache" + str(cc.id+1) + " for address " + str(address))
            f.close()
            cc.data(address, data, "modified")
            
        if state == "owned":
            if (address not in cc.cache.content) or cc.cache.content[address]["state"] != "owned":
                owner = self.CacheController_list[ self.directory.content[address]["owner"]]
                self.directory.content[address]["state"] = "modified"
                self.directory.content[address]["owner"] = cc.id
                self.directory.content[address]["sharer_list"][cc.id] = 0
                # owner = self.CacheController_list[cc.id]
                f = open ("Log_output\SystemLogs.txt", "a")
                f.write(", DirectoryController transact Fwd-GetModified (Fwd-getM) for address " + str(address) + "to Cache" + str(owner.id+1))
                f.close()
                owner.fwd_getM(cc, address)
                ##send invalidation to ones in shared state
                f = open ("Log_output\SystemLogs.txt", "a")
                for i in range(4):
                    if self.directory.content[address]["sharer_list"][i] == 1:
                        f.write(", DirectoryController Invalidated address " + str(address) + " from Cache" + str(self.CacheController_list[i].id+1))
                        self.CacheController_list[i].dir_inv(address)
                        self.directory.content[address]["sharer_list"][i] = 0
                f.close()
            else:
                self.directory.content[address]["state"] = "modified"
                self.directory.content[address]["owner"] = cc.id
                self.directory.content[address]["sharer_list"][cc.id] = 0
                f = open ("Log_output\SystemLogs.txt", "a")
                for i in range(4):
                    if self.directory.content[address]["sharer_list"][i] == 1:
                        f.write(", DirectoryController Invalidated address " + str(address) + " from Cache" + str(self.CacheController_list[i].id+1))
                        self.CacheController_list[i].dir_inv(address)
                        self.directory.content[address]["sharer_list"][i] = 0 
                f.close()
       

    def put(self, cc , address):       
        f = open ("Log_output\SystemLogs.txt", "a")
        state = self.directory.content[address]["state"]
        self.NumDirectoryUpdates += 1 ## Updating Directory
        if state == "modified":
            self.directory.content[address]["owner"] = -1
            self.directory.content[address]["state"] = "invalid"
            f.write(", DirectoryController Invalidated address " + str(address) + " from Cache" + str(cc.id+1))
            f.close()
            cc.dir_inv(address)
        if state == "shared" or state == "invalid":
            self.directory.content[address]["owner"] = -1
            f.write(", DirectoryController Invalidated address " + str(address) + " from Cache" + str(cc.id+1))
            f.close()
            cc.dir_inv(address)
            self.directory.content[address]["sharer_list"][cc.id] = 0
            empty_sharer_list = True
            for i in self.directory.content[address]["sharer_list"]:
                if i == 1:
                    empty_sharer_list = False
                    break
            if empty_sharer_list:
                self.directory.content[address]["state"] = "invalid"
            else:
                self.directory.content[address]["state"] = "shared"
        if state == "owned":
            # self.write(address, data)
            self.directory.content[address]["owner"] = -1
            f.write(", DirectoryController Invalidated address " + str(address) + " from Cache" + str(cc.id+1))
            f.close()
            cc.dir_inv(address)
            self.directory.content[address]["sharer_list"][cc.id] = 0
            empty_sharer_list = True
            for i in self.directory.content[address]["sharer_list"]:
                if i == 1:
                    empty_sharer_list = False
                    break
            if empty_sharer_list:
                self.directory.content[address]["state"] = "invalid"
            else:
                self.directory.content[address]["state"] = "shared"

