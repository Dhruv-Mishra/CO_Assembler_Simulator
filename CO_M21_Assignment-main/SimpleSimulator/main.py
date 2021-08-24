from sys import stdin
from matplotlib import pyplot

memory = []
f1 = stdin.read().split("\n")
for i in f1:
    if (i != ""):
        memory.append(i)
memory = memory + (256 - len(memory)) * [0]
pcl = []


def add(s):
    registers[reg[s[2:5]]] = registers[reg[s[5:8]]] + registers[reg[s[8:11]]]
    if (registers[reg[s[2:5]]] > max_val):
        registers[reg[2:5]] = int(bin(int(registers[reg[s[2:5]]]))[2:][-16:], 2)
        registers[7][0] = 1


def sub(s):
    registers[reg[s[2:5]]] = registers[reg[s[5:8]]] - registers[reg[s[8:11]]]
    if registers[reg[s[2:5]]] < min_val:
        registers[reg[s[2:5]]] = 0
        registers[7][0] = 1


def mul(s):
    registers[reg[s[2:5]]] = registers[reg[s[5:8]]] * registers[reg[s[8:11]]]
    if registers[reg[s[2:5]]] > max_val:
        registers[reg[s[2:5]]] = int(bin(int(registers[s[reg[2:5]]]))[2:][-16:], 2)
        registers[7][0] = 1


def xor(s):
    registers[reg[s[2:5]]] = registers[reg[s[5:8]]] ^ registers[reg[s[8:11]]]


def Or(s):
    registers[reg[s[2:5]]] = registers[reg[s[5:8]]] | registers[reg[s[8:11]]]


def And(s):
    registers[reg[s[2:5]]] = registers[reg[s[5:8]]] & registers[reg[s[8:11]]]


def movimm(s):
    registers[reg[s[:3]]] = int(s[3:], 2)


def rs(s):
    registers[reg[s[:3]]] >> int(s[3:], 2)
    if registers[reg[s[:3]]] > max_val:
        registers[reg[s[:3]]] = int(bin(int(registers[s[reg[:3]]]))[2:][-16:], 2)
        registers[7][0] = 1


def ls(s):
    registers[reg[s[:3]]] << int(s[3:], 2)
    if registers[reg[s[:3]]] > max_val:
        registers[reg[s[0:3]]] = int(bin(int(registers[reg[s[:3]]]))[2:][-16:], 2)
        registers[7][0] = 1


def Not(s):
    x = ""
    for i in s:
        x += str(int(i) ^ 1)
    num = int(x, 2)
    registers[reg[s[5:8]]] = num


def div(s):
    registers[0] = registers[reg[s[5:8]]] // registers[reg[s[8:11]]]
    registers[1] = registers[reg[s[5:8]]] % registers[reg[s[8:11]]]


def movreg(s):
    if reg[s[8:]] != 7:
        registers[reg[s[5:8]]] = registers[reg[s[8:]]]
    else:
        registers[reg[s[5:8]]] = int("".join(list(map(str, registers[7]))), 2)


def cmp(s):
    if registers[reg[s[5:8]]] == registers[reg[s[8:]]]:
        registers[7][3] = 1
    elif registers[reg[s[5:8]]] > registers[reg[s[8:]]]:
        registers[7][2] = 1
    else:
        registers[7][1] = 1


def load(s):
    registers[reg[s[:3]]] = memory[int(s[3:], 2)]


def store(s):
    memory[int(s[3:], 2)] = registers[reg[s[:3]]]


def je(s):
    global pc
    if (registers[7][3]) == 1:
        pc = int(s[3:], 2) - 1


def jlt(s):
    global pc
    if registers[7][1] == 1:
        pc = int(s[3:], 2) - 1


def jgt(s):
    global pc
    if registers[7][2] == 1:
        pc = int(s[3:], 2) - 1


def jmp(s):
    global pc
    pc = int(s[3:], 2) - 1


max_val = 65535
pc = 0
min_val = 0
reg = {"000": 0, "001": 1, "010": 2, "011": 3, "100": 4, "101": 5, "110": 6, "111": 7}
registers = [0] * 7 + [[0, 0, 0, 0]]  # [[overflow],[less than],[greater than],[equal to]]
opcode = {"00000": add, "00001": sub, "00110": mul, "01010": xor, "01011": Or, "01100": And, "00010": movimm,
          "01000": rs, "01001": ls, "00011": movreg, "00111": div, "01101": Not, "01110": cmp, "00100": load,
          "00101": store, "01111": jmp, "10000": jlt, "10001": jgt, "10010": je}


def _8bit(n):  # Function to convert a binary number to 8 bit binary number
    x = bin(n)[2:]
    return "0" * (8 - len(x)) + x


def _16bit(n):  # Function to convert a binary number to 16 bit binary number
    x = bin(n)[2:]
    return "0" * (16 - len(x)) + x

old_pc = 0

while (memory[pc][:5] != "10011"):
    old_pc = pc
    pc2 = pc
    opcode[memory[pc][:5]](memory[pc][5:])
    if old_pc != pc:
        pc2 = pc
        pc = old_pc

    if (memory[pc][:5] != "01110" and registers[7][0] != 1):  # resets flag after instruction if the instruction is not compare or if there is no overflow
        registers[7] = [0, 0, 0, 0]
    print(_8bit(pc), end=" ")
    for i in registers[:7]:
        print(_16bit(i), end=" ")
    print("0" * 12, end="")
    for i in registers[7]:
        print(i, end="")
    print()
    if (registers[7][0] == 1):
        registers[7] = [0, 0, 0, 0]

    pcl.append(pc)
    pc = pc2
    pc = pc + 1

pcl.append(pc)
print(_8bit(pc), end=" ")
for i in registers[:7]:
    print(_16bit(i), end=" ")
print("0" * 12, end="")
for i in registers[7]:
    print(i, end="")
print()
x = range(len(pcl))
for i in memory:
    if (type(i) == type("a")):
        print(i)
    else:
        print(_16bit(i))
pyplot.scatter(x, pcl)
pyplot.xlabel("Cycle Number")
pyplot.ylabel("Program Counter")
pyplot.grid()
pyplot.show()
# assuming st has the instruction line in binary

