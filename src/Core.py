from CacheController import CacheController

class Core:
    def __init__(self, id, CacheController=None):
        self.CacheController = CacheController
        self.id = id

    def connect(self, CacheController : CacheController):
        self.CacheController = CacheController

    def execute(self, inst):

        f = open ("Log_output\SystemLogs.txt", "a")
        f.write("\n\nCore" + str(self.id+1) + ", ")
        if inst[0] == "LS":
            f.write("Requested read-only for address " + str(inst[1]))
            f.close()
            self.CacheController.core_fetch_read(eval(inst[1]))
        if inst[0] == "LM":
            f.write("Requested read-write for address " + str(inst[1]))
            f.close()
            self.CacheController.core_fetch_read_write(eval(inst[1]))
        if inst[0] == "PUT":
            f.write("Invalidate address " + str(inst[1]))
            f.close()
            self.CacheController.core_inv(eval(inst[1]))
        if inst[0] == "ADD":
            f.write("Requested read-write for address " + str(inst[1]))
            f.close()
            value = self.CacheController.core_fetch_read_write(eval(inst[1]))
            value = value + eval(inst[2])
            f = open ("Log_output\SystemLogs.txt", "a")
            f.write(", Core "+str(self.id+1)+" Issued write for address " + str(inst[1]))
            f.close()
            self.CacheController.core_write(eval(inst[1]), value)
        
    
    def getAvgMemoryAccessLatency(self):
        return 1 + (self.getMissRate()*2)
    
    def getMissRate(self):
        if self.CacheController.cacheRequest == 0:
            return self.CacheController.cacheRequest
        return self.CacheController.cacheMiss/self.CacheController.cacheRequest
