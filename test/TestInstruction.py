import random
import sys

cores = [1,2,3,4]
instructions = ["LS", "LM", "PUT", "ADD"]
addresses = [int(i) for i in range(64)]
imm = random.randrange(0, 100)

f = open("instruction_file.txt", "w")

for i in range (int(sys.argv[1])):
    
    core_number = random.randrange(0, 4)
    instruction_number = random.randrange(0, 4)
    # instruction_number = 1

    address_number = random.randrange(0, 64)

    core = cores[core_number]
    instruction = instructions[instruction_number]
    address = addresses[address_number]
    if i != 0:
        f.write("\n")
    if instruction_number != 3:
        line = "core" + str(core) + " " + str(instruction) + " " + str(address)
        f.write(line)
    if instruction_number == 3:
        line = "core" + str(core) + " " + str(instruction) + " " + str(address) + " " +str(imm)
        f.write(line)
f.close()
print("Successfuly Wrote ",sys.argv[1], " random instructions to 'instruction_file.txt'.")
