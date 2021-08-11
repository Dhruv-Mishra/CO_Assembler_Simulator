f = open("input.txt", "r+")
l = f.readlines()
opcode = {"add": ("00000", "RRR"),"sub": ("00001", 'RRR'),"mov": ("00010", 'R$', "00011", 'RR'),"ld": ("00100", "Rm"),"st": ("00101", "Rm"),"mul": ("00110", "RRR"),"div": ("00111", "RR"),"rs": ("01000", "R$"),"ls": ("01001", "R$"),"xor": ("01010", "RRR"),"or": ("01011", "RRR"),"and": ("01100", "RRR"),"not": ("01101", "RR"),"cmp": ("01110", "RR"),"jmp": ("01111", "m"),"jlt": ("10000", "m"),"jgt": ("10001", "m"),"je": ("10010", "m"),"hlt": ("10011", "F")}
registers = {"R0": "000","R1": "001","R2": "010","R3": "011","R4": "100","R5": "101","R6": "110","FLAGS": "111"}
var_dict = {}  # Stores the variable name with the memory address allocated to the variable
label_dict  = {} #Stores the variable name with the memory address allocated to the label
instruction_count = 0
l2 = []
error=False
def _8bit(n):  # Function to convert a binary number to 8 bit binary number
    x = bin(n)[2:]
    num = 8 - len(x)
    return "0" * num + x
def inst_to_bin(instruction_list):
    binary_instruction = ""
    # getting opcode
    if instruction_list[0] in opcode.keys():
        if instruction_list[0] != "mov":
            binary_instruction = binary_instruction + opcode[instruction_list[0]][0]
        else:
            if instruction_list[2][0] == "$":
                binary_instruction += opcode[instruction_list[0]][0]
            else:
                binary_instruction += opcode[instruction_list[0]][2]
        if instruction_list[0] != "mov": # getting type and values accordingly
            if opcode[instruction_list[0]][1] == "RRR":  # type A
            
              if len(instruction_list) == 4 and instruction_list[1] in registers.keys() and instruction_list[2] in registers.keys() and instruction_list[3] in registers.keys():
                
                if registers[instruction_list[1]] != "111" and registers[instruction_list[2]] != "111" and registers[instruction_list[3]] != "111":
                  binary_instruction = binary_instruction + "00" + registers[instruction_list[1]] + registers[instruction_list[2]] + registers[instruction_list[3]]
                  print(binary_instruction)
                else:
                  error = True
                  print("Illegal use of FLAGS register")

              else: 
                error =  True
                print("invalid syntax")
                
            elif opcode[instruction_list[0]][1] == "R$":  # type B
            
                if len(instruction_list) == 3 and 0 <= int(instruction_list[2][1:]) >= 255 and instruction_list[1] in registers.keys():
                                    
                    if registers[instruction_list[1]] != "111":           
                      binary_instruction = binary_instruction + registers[instruction_list[1]] + _8bit(instruction_list[2])
                      print(binary_instruction)
                    else:
                      error = True
                      print("Illegal use of FLAGS register")   
                      
                else:  
                  error =  True
                print("invalid syntax")

            elif opcode[instruction_list[0]][1] == "RR":  # type C

              if len(instruction_list) == 3 and instruction_list[1] in registers.keys() and instruction_list[2] in registers.keys():
                
                if registers[instruction_list[1]] != "111" and registers[instruction_list[2]] != "111":
                  binary_instruction = binary_instruction + "00000" + registers[instruction_list[1]] + registers[instruction_list[2]]
                  print(binary_instruction)
                else:
                  error = True
                  print("Illegal use of FLAGS register")   

              else:
                error =  True
                print("invalid syntax")

            elif opcode[instruction_list[0]][1] == "Rm":  # type D

              if len(instruction_list) == 3 and instruction_list[1] in registers.keys():  

                if registers[instruction_list[1]] != "111":
                  if instruction_list[2] in var_dict.keys():
                    binary_instruction = binary_instruction + registers[instruction_list[1]] + var_dict[instruction_list[2]]
                    print(binary_instruction)
                  else:
                    error = True
                    print("Use of undefined variable")
                else:
                  error = True
                  print("Illegal use of FLAGS register") 

              else:
                error =  True
                print("invalid syntax")

            elif opcode[instruction_list[0]][1] == "m":  # type E
              if instruction_list[1] in label_dict:
                binary_instruction = binary_instruction + "000" + label_dict[instruction_list[1]]
                print(binary_instruction)
              else:
                print("label undefined")
            elif opcode[instruction_list[0]][1] == "F":  # type F
                binary_instruction = binary_instruction + "0" * 11
                print(binary_instruction)
        else:
            if instruction_list[2][0] == "$":

              if len(instruction_list) == 2 and instruction_list[1] in registers.keys():
        
                if registers[instruction_list[1]] != "111":
                  binary_instruction = binary_instruction + registers[instruction_list[1]] + _8bit(int(instruction_list[2][1:]))
                  print(binary_instruction)
                else:
                  error = True
                  print("Illegal use of FLAGS register")
              
              else:
                error =  True
                print("invalid syntax")

            else:

                binary_instruction = binary_instruction + "00000" + registers[instruction_list[1]] + registers[instruction_list[2]]
                print(binary_instruction)


for i in l:  # Gives final list of instructions without empty lines
    if i != '''\n''':
        l2.append(i)
        if (i.strip().split()[0] in opcode):  # Count of the total number of instructions excluding var and label declerations
            instruction_count += 1
        elif (i.strip().split()[0][-1] == ":"):  # identifying a label declaration
            if (i.strip().split()[0][:-1] not in label_dict):
                label_dict[i.strip().split()[0][:-1]] = _8bit(instruction_count)
                instruction_count += 1
hlt_chk=l2[-1].strip().split()
if(len(hlt_chk)==2):                                          #Checking that program ends with halt statement
  if(hlt_chk[0][-1]==":" and hlt_chk[1]=="hlt"):
    pass
  else:
    print("[ERROR] Program does not end with halt statement")
    error=True
elif(len(hlt_chk)==1):
  if(hlt_chk[0]!="hlt"):
    print("[ERROR] Program does not end with halt statement")
    error=True
  elif(hlt_chk[0]=="hlt"):
    pass
  else:
    print("[ERROR] Program does not end with halt statement")
    error=True
else:
  print("[ERROR] Program does not end with halt statement")
  error=True
pre_var_dec=True
for i in l2[:-1]:
    tempvar = i.strip().split()
    if (tempvar[0] == "var" and pre_var_dec):  # identifying a variable declaration
        if (tempvar[1] not in var_dict):
            var_dict[tempvar[1]] = _8bit(instruction_count)
            instruction_count += 1
        else:
            print("Variable already exists")   #[ERROR] Redecleration of same variable
            error=True
            break
    elif(tempvar[0] == "var" and not pre_var_dec):
      print("Variable not declared at the start")  #[ERROR] Variable not declared at the start 
      error=True
      break
    else:
      pre_var_dec=False
    if(tempvar[0]=="hlt"):
      print("[ERROR] Halt statement used before termination")
      error=True
      break
    elif(tempvar[0][-1]==":" and tempvar[1]=="hlt"):
      error=True
      print("[ERROR] Halt statement used before termination")
      break
      
for i in l2:
    instruction_list = i.strip().split()
    # getting opcode
    if (instruction_list[0] != "var" and instruction_list[0][-1] != ":"):
        inst_to_bin(instruction_list)
    elif (instruction_list[0][-1] == ":"):
        if len(instruction_list[1:]) > 0:
          inst_to_bin((instruction_list[1:]))
