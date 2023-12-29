import random

class CacheController:
    def __init__(self, id, cache=None, core=None, directory_controller=None):
        self.id = id
        self.cache = cache
        self.core = core
        self.directory_controller = directory_controller
        self.cacheHit = 0
        self.cacheMiss = 0
        self.cacheRequest = 0 # Just to verify CacheRequest == CacheMiss + CacheHit

    def connect(self, cache , core, directory_controller):
        self.cache = cache
        self.core = core
        self.directory_controller = directory_controller

    def fetchCachedData(self, address):
        self.cache.content[int(address)%2]["NotLRU"] = address ## Since 2 way set assoc, the other is always LRU
        return self.cache.content[int(address)%2][address]["data"]
    
    def fetchCachedState(self, address):
        # self.cache.content[int(address)%2]["NotLRU"] = address ## Since 2 way set assoc, the other is always LRU
        return self.cache.content[int(address)%2][address]["state"]
    
    def updateCachedData(self, address, state, data):
        self.cache.content[int(address)%2]["NotLRU"] = address

        if state == "invalid":
            self.cache.content[int(address)%2][address] = {}
            return
        
        if data != None:
            try:
                self.cache.content[int(address)%2][address]["data"] = data  
            except KeyError:
                self.cache.content[int(address)%2][address] = {}
                self.cache.content[int(address)%2][address]["data"] = data

        if state != None:
            try:
                self.cache.content[int(address)%2][address]["state"] = state    
            except KeyError:
                self.cache.content[int(address)%2][address] = {}
                self.cache.content[int(address)%2][address]["state"] = state

        
    def fwd_getS(self, cc, address):
        f = open ("Log_output\SystemLogs.txt", "a")

        requestor_state = None
        if address in cc.cache.content[int(address)%2]:
            requestor_state = self.fetchCachedState(address)
        
        self.updateCachedData(address, "owned", None)
        data = self.fetchCachedData(address)

        self.updateCachedData(address, "shared", None)
        if requestor_state == "modified":
            f.write(", CacheController"+ str(self.id+1) + " sent "+ str(data) +"with State Owned to Cache" + str(cc.id+1) + " for address " + str(address))
            f.close()
            cc.data(address, data, "owned")
        else:
            f.write(", CacheController"+ str(self.id+1) + " sent "+ str(data) +"with State Shared to Cache" + str(cc.id+1) + " for address " + str(address))
            f.close()
            cc.data(address, data, "shared")

        

    def fwd_getM(self, cc, address):
        f = open ("Log_output\SystemLogs.txt", "a")

        data = self.fetchCachedData(address)
        self.updateCachedData(address, "invalid", None)
        # self.cache.content[address]["state"] = "invalid"
        
        # data = self.cache.content[address]["data"]

        #TODO - Check below for any change
        f.write(", CacheController"+ str(self.id+1) + " sent "+ str(data) +"with State Modified to Cache" + str(cc.id+1) + " for address " + str(address))
        f.close()
        cc.data(address, data, "modified")
        

    
    # Change Here -> Fully Assoc to 2 Way assoc
    def data(self, address, data, final_state):
        # first check if there's space otherwise put and then write
        if address in self.cache.content[int(address)%2]:
            self.updateCachedData(address, final_state, data)
            # self.cache.content[address]["data"] = data
            # self.cache.content[address]["state"] = final_state
        else:
            # Check if space is available in Cache
            for _address in self.cache.content[int(address)%2]:
                if _address != "NotLRU" and not self.cache.content[int(address)%2][_address]:     
                    del self.cache.content[int(address)%2][_address]
                    self.updateCachedData(address, final_state, data)
                    return
            
            # LRU Eviction Policy
            for _address in self.cache.content[int(address)%2]:
                if _address != "NotLRU" and _address != self.cache.content[int(address)%2]["NotLRU"]: # if NotLRU then other is LRU
                    self.directory_controller.put(self, _address)
                    del self.cache.content[int(address)%2][_address]
                    self.updateCachedData(address, final_state, data)
                    return

    def core_write(self, address, data):
        self.updateCachedData(address, None, data)
        # self.cache.content[address]["data"] = data
        
        
        #TODO - Check below for any change
        # write to the memory without a worry
        self.directory_controller.write(address, data)

    def core_fetch_read(self, address):  # getS
        f = open ("Log_output\SystemLogs.txt", "a")
        self.cacheRequest += 1
        # check if there's any need to call getS

        if address in self.cache.content[int(address)%2] and self.cache.content[int(address)%2][address] and self.fetchCachedState(address) == "shared":
        # if address in self.cache.content and self.cache.content[address]["state"] == "shared":
            self.cacheHit += 1
            f.close()
            return self.fetchCachedData(address)
        else:
            # print(self)
            self.cacheMiss += 1
            f.write(", CacheController"+ str(self.id+1) +" transact GetShared (getS) for address " + str(address))
            f.close()
            self.directory_controller.getS(self, address)
        

    def core_fetch_read_write(self, address):  # getM
        f = open ("Log_output\SystemLogs.txt", "a")
        # check if there's any need to call getM'
        self.cacheRequest += 1

        if address in self.cache.content[int(address)%2] and self.cache.content[int(address)%2][address] and self.fetchCachedState(address) == "modified":
            # if self.cache.content[address]["state"] == "modified":
            self.cacheHit += 1
            f.close()
            return self.fetchCachedData(address)
        else:
            self.cacheMiss += 1
            f.write(", CacheController"+ str(self.id+1) +" transact GetModified (getM) for address " + str(address))
            f.close()
            self.directory_controller.getM(self, address)
            
            return self.fetchCachedData(address)
        

    def core_inv(self, address):  # put
        # check if there's any need to call put
        if address in self.cache.content[int(address)%2]:
        # if address in self.cache.content:
            f = open ("Log_output\SystemLogs.txt", "a")
            f.write(", CacheController"+ str(self.id+1) +" transact Put for address " + str(address))
            f.close()
            self.directory_controller.put(self, address)
        else:
            return 0

    def dir_inv(self, address):
        # self.cache.content[address]["state"] = "invalid"
        self.updateCachedData(address, "invalid", None)
