from Core import Core
from Cache import Cache
from CacheController import CacheController
from DirectoryController import DirectoryController
from Directory import Directory
from Memory import Memory
import matplotlib.pyplot as plt
import numpy as np

# initialize the components

directoryUpdates = []

core1 = Core(0)
core2 = Core(1)
core3 = Core(2)
core4 = Core(3)

cache1 = Cache(size=4)
cache2 = Cache(size=4)
cache3 = Cache(size=4)
cache4 = Cache(size=4)

CacheController1 = CacheController(0)
CacheController2 = CacheController(1)
CacheController3 = CacheController(2)
CacheController4 = CacheController(3)

DirectoryController0 = DirectoryController()

directory0 = Directory(size=64)
memory0 = Memory(size=64)

# connect the components
core1.connect(CacheController1)
core2.connect(CacheController2)
core3.connect(CacheController3)
core4.connect(CacheController4)

cache1.connect(CacheController1)
cache2.connect(CacheController2)
cache3.connect(CacheController3)
cache4.connect(CacheController4)

CacheController1.connect(cache1, core1, DirectoryController0)
CacheController2.connect(cache2, core2, DirectoryController0)
CacheController3.connect(cache3, core3, DirectoryController0)
CacheController4.connect(cache4, core4, DirectoryController0)

DirectoryController0.connect(directory0, memory0, [CacheController1, CacheController2, CacheController3, CacheController4])

directory0.connect(DirectoryController0, memory0)
memory0.connect(directory0, DirectoryController0)




def getDirectoryUpdates():
    return DirectoryController0.NumDirectoryUpdates

def plotMissRatesValues():
    dataValues = []
    for _core in [core1, core2, core3, core4]:
        dataValues.append(_core.getMissRate())

    x_labels = [f"core{i}" for i in range(0, len(dataValues))]

    plt.bar(range(len(dataValues)), list(dataValues))

    plt.ylabel("Miss Rate latency")
    plt.title("Miss Rate Vs Core")

    plt.xticks(range(len(x_labels)), x_labels)

    plt.savefig("Plots\{}.jpg".format("MissRate_Vs_Core"))
    plt.clf()

def plotAverageMissLatencyValues():
    dataValues = []
    for _core in [core1, core2, core3, core4]:
        dataValues.append(_core.getAvgMemoryAccessLatency())

    x_labels = [f"core{i}" for i in range(0, len(dataValues))]

    plt.bar(range(len(dataValues)), list(dataValues))

    plt.ylabel("Avg Memory access latency")
    plt.title("Avg Memory access latency Vs Core")

    plt.xticks(range(len(x_labels)), x_labels)

    plt.savefig("Plots\{}.jpg".format("Avg_Memory_access_latency_Vs_Core"))
    plt.clf()

    
def plotDirectoryUpdates(data_array):
    x_values = np.arange(len(data_array))

    # Plotting the line graph
    plt.plot(x_values, data_array, marker='o', linestyle='-')

    # Adding labels and title
    plt.xlabel("time")
    plt.ylabel("Number of Directory Updates")
    plt.title("Number of Directory Updates Vs Time")

    plt.savefig("Plots\{}.jpg".format("Directory_Updates_Vs_Time"))
    plt.clf()


def executeInstruction():
    f = open ("Log_output\CacheLogs.txt", "w")
    t = open ("Log_output\SystemLogs.txt", "w")
    t.close()
    with open("instruction_file.txt", "r") as file:
        i = 1
        print("Executing Instructions...")
        for instruction in file:
            # print(i)
            inst_list = instruction.split(" ")
            if inst_list[0] == "core1":
                core1.execute(inst_list[1:])
            elif inst_list[0] == "core2":
                core2.execute(inst_list[1:])
            elif inst_list[0] == "core3":
                core3.execute(inst_list[1:])
            elif inst_list[0] == "core4":
                core4.execute(inst_list[1:])

            f.write("Caches After Instruction {}: {}".format(i,instruction.split("\n")[0]) + "\n")
            f.write("Cache1 " + str(cache1.content) + "\n")
            f.write("Cache2 " + str(cache2.content) + "\n")
            f.write("Cache3 " + str(cache3.content) + "\n")
            f.write("Cache4 " + str(cache4.content) + "\n\n")
            directoryUpdates.append(getDirectoryUpdates())
            i+=1

    f.close()
    for i in memory0.content:
        print ("Memory address: " + str(i) + "    Value stored: " + str(memory0.content[i]) + "    Directory Entry: " + str(directory0.content[i]))


executeInstruction()
plotMissRatesValues()
plotAverageMissLatencyValues()
plotDirectoryUpdates(directoryUpdates)