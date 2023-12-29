class Cache:
    def __init__(self, size, CacheController=None):
        cache_contents = [
            {
                -1:{},
                -2:{},
                "NotLRU":-1
            },
            {
                -1:{},
                -2:{},
                "NotLRU":-1
            }
        ]

        # for i in range(size):
        #     cache_contents[i] = {"data": 0, "state": "invalid"}
            
        self.content = cache_contents
        self.CacheController = CacheController

    def connect(self, CacheController):
        self.CacheController = CacheController
