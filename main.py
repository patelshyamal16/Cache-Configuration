import math
count = 0
loopcounter = 1
jcounter = 1
loopcounter1 = 1
jcounter2 = 1
TotalInstructionCounter = 0
ALUCounter = 0
JumpCounter = 0
MemoryCounter = 0
OtherCounter = 0
SpecialCounter = 0
BranchCounter = 0
Hit = 0
Miss = 0
cacheConfig = 0

#-------------This is for case 1-4 of project 4-------------
ValidBits =   [0,  0,  0,  0,  0,  0,  0,  0] #Initialize all valid bits to be 0 at first
validBits3 = [[0,0],[0,0],[0,0],[0,0]]
validBits4 = [[0,0,0,0],[0,0,0,0]]
tagList =     [0,  0,  0,  0,  0,  0,  0,  0] #Intialize all keys to be 0 at first
tagList3 = [[0,0],[0,0],[0,0],[0,0]]
tagList4 = [[0,0,0,0],[0,0,0,0]]
data =        [0,  0,  0,  0,  0,  0,  0,  0] #Intialize all data to be 0 at first
LRU = [0,1,2,3,4,5,6,7]
twoW4setLRU = [0,0,0,0]
fourW2setLRU0 = [0,1,2,3]
fourW2setLRU1 = [0,1,2,3]
#             000 001 010 011 100 101 110 111 <------Cache index corresponding to each array
#---------------------------------------------------------
def twosCompliment(binValue, numOfBits):
    binValue = binValue - (1 << numOfBits)
    return binValue


def hextobin(c):
    num = int(c, base=16)
    b = bin(num)
    return (b[2:].zfill(4))


def parse_hex8(s):
    b = ""
    for i in range(8):
        b += hextobin(s[i])
    return b


A_addr = [i for i in range(0x2000, 0x3004, 4)]
memory = dict.fromkeys(A_addr, 0)


def addi(rs, rt, imm):
    rt = rs + imm
    return rt


def ori(rs, rt, imm):
    rt = rs | imm
    return rt


def andi(rs, rt, imm):
    rt = rs & imm
    return rt


def lw(rs, rt, imm):
    memoryLocation = rs + imm
    for memoryKey, memoryValue in memory.items():
        if memoryLocation == memoryKey:
            DMVALUE = memoryValue
            rt = DMVALUE
    return rt


def Add(rs, rt, rd):
    rd = rs + rt
    return rd


def And(rs, rt, rd):
    rd = rs & rt
    return rd


def sll(rt, rd, sh):
    rd = rt << sh
    return rd


def srl(rt, rd, sh):
    rd = rt >> sh
    return rd


def sra(rt, rd, sh):
    rd = rt >> sh
    return rd


def sub(rs, rt, rd):
    rd = rs - rt
    return rd


def Or(rs, rt, rd):
    rd = rs | rt
    return rd


def Xor(rs, rt, rd):
    rd = rs ^ rt
    return rd


def xori(rs, rt, imm):
    rt = rs ^ imm
    return rt


def sw(rs, rt, imm):
    memoryLocation = rs + imm
    for memoryKey, memoryValue in memory.items():
        if memoryLocation == memoryKey:
            memoryKey = rt
    return rt


def branchnotequal(rs, rt, imm, programCounter):

    if (rs != rt):
        programCounter += (imm * 4)
    return programCounter


def branchequal(rs, rt, imm, programCounter):
    if (rs == rt):
        programCounter += (imm * 4)
    return programCounter


def Jump(imm, programCounter):
    programCounter = (imm - 4)
    return programCounter


def lui(rt, imm):
    rt = imm << 16
    return rt


def slt(rs, rt, rd):
    if (rs < rt):
        rd = 1
    else:
        rd = 0
    return rd


def match(rs, rt, rd):
    rd = 0

    if rt >= 0:
        rt = bin(rt)[2:].zfill(32)
    else:
        rt = bin(rt)[3:].zfill(32)
        rt = twosCompliment(int(rt, 2), len(rt))
        rt = bin(rt)[3:].zfill(32)

    if rs >= 0:
        rs = bin(rs)[2:].zfill(32)
    else:
        rs = bin(rs)[3:].zfill(32)
        rs = twosCompliment(int(rs, 2), len(rs))
        rs = bin(rs)[3:].zfill(32)

    for i in range(len(rs)):
        if rs[i] == rt[i]:
            rd += 1
    return rd


def immALU(opcode, rs, rt, imm, programCounter):
    ALUoperations = {
        4: branchequal(rs, rt, imm, programCounter),  #complete
        5: branchnotequal(rs, rt, imm, programCounter),  #complete
        2: Jump(imm, programCounter),  #complete
        8: addi(rs, rt, imm),  #complete
        12: andi(rs, rt, imm),  #complete
        13: ori(rs, rt, imm),  #complete
        14: xori(rs, rt, imm),  #complete
        15: lui(rt, imm),  #complete
        35: lw(rs, rt, imm),  #complete
    }

    for key2, value2 in ALUoperations.items():
        if key2 == opcode:
            finalresult = value2
            return finalresult


def funcALU(funccode, rs, rt, rd, sh, programCounter):
    ALUoperations = {
        0: sll(rt, rd, sh),  #complete
        2: srl(rt, rd, sh),  #complete
        3: sra(rt, rd, sh),
        32: Add(rs, rt, rd),  #complete
        34: sub(rs, rt, rd),  #complete
        36: And(rs, rt, rd),  #complete
        37: Or(rs, rt, rd),  #complete
        38: Xor(rs, rt, rd),  #complete
        42: slt(rs, rt, rd),
        1: match(rs, rt, rd)
    }

    for key3, value3 in ALUoperations.items():
        if key3 == funccode:
            finalresult2 = value3
            return finalresult2


opcodes = {  #reference for opcode bits
    0: "R-Type",
    2: "j",
    4: "beq",
    5: "bne",
    8: "addi",
    12: "andi",
    13: "ori",
    14: "xori",
    15: "lui",
    35: "lw",
    43: "sw"
}

functionCodes = {  #reference for r-type instructions
    0: "sll",
    1: "match",  # special Instr
    2: "srl",
    3: "sra",
    32: "add",
    34: "sub",
    36: "and",
    37: "or",
    38: "xor",
    42: "slt"
}
registerFile = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
    21: 0,
    22: 0,
    23: 0,
    24: 0,
    25: 0,
    26: 0,
    27: 0,
    28: 0,
    29: 0,
    30: 0,
    31: 0,
    "Hi": 0,
    "Lo": 0,
    "PC": 0
}


def generateBinaryInst():
    print('Reading in text file...')
    f = open('prog.asm')
    lines = f.readlines()
    f.close()
    binaryInstructions = []  #list to hold binary instr...
    # result1 = []
    for line in lines:  #convert lines from hex to binary
        buffer = parse_hex8(line)
        binaryInstructions.append(buffer)
        print(line + "Binary-> " + buffer + "\n")
    return binaryInstructions


def memoryInstruction(binaryFile):
    sizeOfFile = 4 * len(binaryFile)
    instructionAddress = [i for i in range(0, sizeOfFile, 4)]
    instructionDict = dict(zip(instructionAddress, binaryFile))
    return instructionDict


def printResults(registerDict, memoryDict):
    global TotalInstructionCounter
    print('-------------------------------------------------')
    print('----------------Registers------------------------')
    print('-------------------------------------------------')
    for register, registerValue in registerDict.items():
        if (register == "Hi" or register == "Lo" or register == "PC"):
            print(f'\t\t\t      {register} : {registerValue}')
        else:
            print(f'\t\t\t     ${register} : {registerValue}')
    print('-------------------------------------------------')
    print('----------------DATA MEMORY----------------------')
    print('-------------------------------------------------')
    for i in range(0x2000, 0x2070, 4):
        for memoryLocation, memoryValue in memoryDict.items():
            if i == memoryLocation:
                print(f'\t\t\tDM[{i}] : {memoryValue}')
    print('-------------------------------------------------')
    print('--------------Instruction Statistics-------------')
    print('-------------------------------------------------')
    print(f'\t\t\tTotal:\t{TotalInstructionCounter}')
    print(
        f'\t\t\tALU:\t{ALUCounter}  {int((ALUCounter/TotalInstructionCounter)*100)}%'
    )
    print(
        f'\t\t\tBranch:\t {BranchCounter}  {int((BranchCounter/TotalInstructionCounter)*100)}%'
    )
    print(
        f'\t\t\tJump:\t {JumpCounter}   {int((JumpCounter/TotalInstructionCounter)*100)}%'
    )
    print(
        f'\t\t\tMemory:\t {MemoryCounter}  {int((MemoryCounter/TotalInstructionCounter)*100)}%'
    )
    print(
        f'\t\t\tOther:\t {OtherCounter}  {int((OtherCounter/TotalInstructionCounter)*100)}%'
    )
    print(
        f'\t\t\tSpecial: {SpecialCounter}   {int((SpecialCounter/TotalInstructionCounter)*100)}%'
    )
    print('-------------------------------------------------')

def DM(N, S, B, rsValue, result):
  global Hit
  global Miss
  global count
  global hitRate 
  
  count+=1
  hexMemAddress = hex(rsValue)
  memAddress = bin(rsValue)[2:].zfill(32)

  offset = int(memAddress[(32 - int((math.log(B))/(math.log(2)))):(len(memAddress))],2)
  index = int(memAddress[32-(int((math.log(S))/(math.log(2))))-(int((math.log(B))/(math.log(2)))):(32 - int((math.log(B))/(math.log(2))))],2)
  tag = memAddress[0:32-(int((math.log(S))/(math.log(2))))-(int((math.log(B))/(math.log(2))))]
  logfile.append(f'{count}) Memory Access Location(Hex): {hexMemAddress}\n    Memory Access Loaction(Bin): {memAddress}\n    BreakDown:\n      -Tag: {tag} ({hex(int(tag,2))})\n      -Set: {index} ({hex(index)})\n      -IN-blk offset:{offset} ({hex(offset)})\n\n')
  
  if(ValidBits[index] == 0):
    Miss +=1
    logfile.append(f'    Trying Set {index} which has Tag: {tag[index]} ({hex(tagList[index])})\n    Cache Miss, Set is empty. Writing data into cache\n    Hit: {Hit}, Miss: {Miss}\n\n')
    tagList[index] = tag 
    ValidBits[index] = 1
    data[index] = result
  else: 
    if(tagList[index] == tag):
      Hit +=1
      logfile.append(f'    Trying Set {index} which has Tag: {tagList[index]} ({hex(int(tagList[index],2))})\n    Cache Hit, Valid bit is 1. Accessing DM\n    Hit: {Hit}, Miss: {Miss}\n\n')
    else:
      Miss +=1
      logfile.append(f'    Cache Miss, Set is Occupied. Writing data into cache\n    Hit: {Hit}, Miss: {Miss}\n\n')
      tagList[index] = tag 
      ValidBits[index] = 1
      data[index] = result

def FA(N,S,B, rsValue, result):
  global Hit
  global Miss
  global count
  global hitRate 
  
  count+=1
  hexMemAddress = hex(rsValue)
  memAddress = bin(rsValue)[2:].zfill(32)

  offset = int(memAddress[(32 - int((math.log(B))/(math.log(2)))):(len(memAddress))],2)
  index = 0
  tag = memAddress[0:32-(int((math.log(S))/(math.log(2))))-(int((math.log(B))/(math.log(2))))]
  logfile.append(f'({count}) Memory Access Location(Hex): {hexMemAddress}\n    Memory Access Loaction(Bin): {memAddress}\n    BreakDown:\n      -Tag: {tag} ({hex(int(tag,2))})\n      -Set: {index} ({hex(index)})\n      -IN-blk offset:{offset} ({hex(offset)})\n')
  
    
    #LRU = [0,1,2,3,4,5,6,7]
   #lJSdhlZshdlad
  while (index < 8):
    
    if(ValidBits[index] == 0):
      Miss +=1
      logfile.append(f'\n    Trying Block {index} Tag:({hex(tagList[index])}) -- Cache Miss, Set is empty.\n    Hit: {Hit}, Miss: {Miss}\n\n')
      tagList[index] = tag 
      ValidBits[index] = 1
      data[index] = result
      #print(LRU)
      LRU.sort(key = index.__eq__)
      #print(LRU)
      index = 8
    else: 
      if(tagList[index] == tag):
        LRU.sort(key = index.__eq__)
        Hit +=1
        logfile.append(f'\n    Trying Block {index} Tag:({hex(int(tagList[index],2))}) -- Cache Hit.\n    Hit: {Hit}, Miss: {Miss}\n\n')
        index = 8

      else:

        if(index == 7):
          
          Miss +=1
          logfile.append(f'\n    Trying block {index} tag {hex(int(tagList[index],2))} -- OCCUPIED.\n')
          logfile.append("    All blocks are occupied, implementing LRU policy...\n")
          logfile.append(f'    replacing block {LRU[0]} since it is the least recently used block\n    Hit: {Hit}, Miss: {Miss}\n\n')
          tagList[LRU[0]] = tag 
          ValidBits[LRU[0]] = 1
          data[LRU[0]] = result
          LRU.sort(key = LRU[0].__eq__)
          index = 8
        else:
          logfile.append(f'    Block {index} -- OCCUPIED.\n')
          index += 1

def config3(N,S,B, rsValue, result):
  global Hit
  global Miss
  global count
  global hitRate 

  count+=1
  hexMemAddress = hex(rsValue)
  memAddress = bin(rsValue)[2:].zfill(32)

  offset = int(memAddress[(32 - int((math.log(B))/(math.log(2)))):(len(memAddress))],2)
  index = int(memAddress[32-(int((math.log(S))/(math.log(2))))-(int((math.log(B))/(math.log(2)))):(32 - int((math.log(B))/(math.log(2))))],2)
  tag = memAddress[0:32-(int((math.log(S))/(math.log(2))))-(int((math.log(B))/(math.log(2))))]
  logfile.append(f'({count}) Memory Access Location(Hex): {hexMemAddress}\n    Memory Access Loaction(Bin): {memAddress}\n    BreakDown:\n      -Tag: {tag} ({hex(int(tag,2))})\n      -Set: {index} ({hex(index)})\n      -IN-blk offset:{offset} ({hex(offset)})\n')
    
    #LRU = [0,1,2,3,4,5,6,7]
   #lJSdhlZshdlad
  
  #check for either way 0 or way 1 for the selected index/set  
  if(validBits3[index][0] == 0):
    Miss +=1
    logfile.append(f'\n    Trying Set {index} Way 0 Tag:({hex(tagList3[index][0])}) -- Cache Miss, Set is empty.\n    Hit: {Hit}, Miss: {Miss}\n\n')
    tagList3[index][0] = tag 
    validBits3[index][0] = 1
    #data[index] = result
    #print(LRU)
    twoW4setLRU[index] = 1 #THe least recently used way of the current set being looked at should be set to 1.
    #print(LRU)
    
  else: 
    if(tagList3[index][0] == tag):
      twoW4setLRU[index] = 1
      Hit +=1
      logfile.append(f'\n    Trying Set {index} Way 0 Tag:({hex(int(tagList3[index][0],2))}) -- Cache Hit.\n    Hit: {Hit}, Miss: {Miss}\n\n')
      
    else:
      if(validBits3[index][1] == 0):
        Miss +=1
        logfile.append(f'\n    Trying Set {index} way 0 Tag:({hex(tagList3[index][1])}) -- Occupied.\n')
        logfile.append(f'\n    Trying Set {index} Way 1 Tag:({hex(tagList3[index][1])}) -- Cache Miss, Set is empty.\n    Hit: {Hit}, Miss: {Miss}\n\n')
        tagList3[index][1] = tag
        validBits3[index][1] = 1
        #data[index] = result
        #print(LRU)
        twoW4setLRU[index] = 0 #THe least recently used way of the current set being looked at should be set to 0.
        #print(LRU)
      
      else: 
        logfile.append(f'\n    Trying Set {index} way 0 Tag:({hex(int(tagList3[index][1],2))}) -- Occupied.\n')
        if(tagList3[index][1] == tag):
          twoW4setLRU[index] = 0
          Hit +=1
          logfile.append(f'\n    Trying Set {index} way 1 Tag:({hex(int(tagList3[index][1],2))}) -- Cache Hit.\n    Hit: {Hit}, Miss: {Miss}\n\n')
        else:
          Miss +=1
          logfile.append(f'\n    Trying Set {index} way 1 tag {hex(int(tagList3[index][1],2))} -- OCCUPIED.\n')
          logfile.append("    All blocks are occupied, implementing LRU policy...\n")
          logfile.append(f'    replacing Set {index} way {twoW4setLRU[index]} since it is the least recently used block\n    Hit: {Hit}, Miss: {Miss}\n\n')
          tagList3[index][twoW4setLRU[index]] = tag 
          #ValidBits[LRU[0]] = 1
          #data[LRU[0]] = result
          twoW4setLRU[index] = twoW4setLRU[index] - 1
          
def config4(N,S,B, rsValue, result):
  global Hit
  global Miss
  global count
  global hitRate 
  
 
  
  count+=1
  hexMemAddress = hex(rsValue)
  memAddress = bin(rsValue)[2:].zfill(32)

  offset = int(memAddress[(32 - int((math.log(B))/(math.log(2)))):(len(memAddress))],2)
  index = int(memAddress[32-(int((math.log(S))/(math.log(2))))-(int((math.log(B))/(math.log(2)))):(32 - int((math.log(B))/(math.log(2))))],2)
  tag = memAddress[0:32-(int((math.log(S))/(math.log(2))))-(int((math.log(B))/(math.log(2))))]
  logfile.append(f'({count}) Memory Access Location(Hex): {hexMemAddress}\n    Memory Access Loaction(Bin): {memAddress}\n    BreakDown:\n      -Tag: {tag} ({hex(int(tag,2))})\n      -Set: {index} ({hex(index)})\n      -IN-blk offset:{offset} ({hex(offset)})\n')
    
    #LRU = [0,1,2,3,4,5,6,7]
   #lJSdhlZshdlad
  blockIndex = 0
  #check for either way 0 or way 1 for the selected index/set
  while(blockIndex < 4):  
    if(validBits4[index][blockIndex] == 0):
      Miss +=1
      logfile.append(f'\n    Trying Set {index} Way {blockIndex} Tag:({hex(tagList4[index][blockIndex])}) -- Cache Miss, Set is empty.\n    Hit: {Hit}, Miss: {Miss}\n\n')
      tagList4[index][blockIndex] = tag 
      validBits4[index][blockIndex] = 1

      #data[index] = result
      #print(LRU)
    
      if(index == 0):
        fourW2setLRU0.sort(key = blockIndex.__eq__)
      else:
        fourW2setLRU1.sort(key = blockIndex.__eq__)
        

      
        #THe least recently used way of the current set being looked at should be set to 1.
      #print(LRU)
      blockIndex = 4
    
    else: 
      #logfile.append(f'\n    Trying Set {index} way {blockIndex} Tag:({hex(int(tagList4[index][blockIndex],2))}) -- Occupied.\n')
      if(tagList4[index][blockIndex] == tag):
        if(index == 0):
          fourW2setLRU0.sort(key = blockIndex.__eq__)
        else:
          fourW2setLRU1.sort(key = blockIndex.__eq__)
        Hit +=1
        logfile.append(f'\n    Trying Set {index} way {blockIndex} Tag:({hex(int(tagList4[index][blockIndex],2))}) -- Cache Hit.\n    Hit: {Hit}, Miss: {Miss}\n\n')
        blockIndex = 4

      else:
        logfile.append(f'\n    Trying Set {index} way {blockIndex} Tag:({hex(int(tagList4[index][blockIndex],2))}) -- OCCUPIED.\n    Hit: {Hit}, Miss: {Miss}\n\n')  
        blockIndex += 1
        if(index == 0):
          fourW2setLRU0.sort(key = blockIndex.__eq__)
        else:
          fourW2setLRU1.sort(key = blockIndex.__eq__) 
      if(blockIndex == 3):
        Miss +=1
        #logfile.append(f'\n    Trying Set {index} way {blockIndex} tag {hex(int(tagList4[index][blockIndex],2))} -- OCCUPIED.\n')
    
        logfile.append("    All blocks are occupied, implementing LRU policy...\n")
        if index == 0:

          logfile.append(f'    replacing Set {index} way {fourW2setLRU0[0]} since it is the least recently used block\n    Hit: {Hit}, Miss: {Miss}\n\n')
        else: 
          logfile.append(f'    replacing Set {index} way {fourW2setLRU1[0]} since it is the least recently used block\n    Hit: {Hit}, Miss: {Miss}\n\n')
        if(index == 0):
          lru0 = fourW2setLRU0[0]
          tagList4[index][lru0] = tag
        else:
        
          tagList4[index][fourW2setLRU1[0]] = tag 
          #ValidBits[LRU[0]] = 1
          #data[LRU[0]] = result
        if(index == 0):
          fourW2setLRU0.sort(key = blockIndex.__eq__)
        else:
          fourW2setLRU1.sort(key = blockIndex.__eq__) 
        blockIndex = 4     
      blockIndex += 1 
      
  
def prog_file(binaryInstruct, programCounter):
    global loopcounter
    global jcounter
    global loopcounter1
    global jcounter2
    global ALUCounter
    global JumpCounter
    global MemoryCounter
    global OtherCounter
    global SpecialCounter
    global BranchCounter
    global TotalInstructionCounter
    global cacheConfig
    instr = binaryInstruct
    newpc = programCounter
    

    for key, value in opcodes.items():
      if int(instr[0:6], 2) == key:
        if key == 0:
          for funcNum, funcCode in functionCodes.items():
            if int(instr[26:32], 2) == funcNum:
              if funcNum == 0 or funcNum == 2 or funcNum == 3:
                rs = 0
                rt = int(instr[11:16], 2)
                rd = int(instr[16:21], 2)
                sh = int(instr[21:26], 2)

                for registerKey, registerValue in registerFile.items(
                ):
                    if rt == registerKey:
                        rtValue = registerValue

                result = funcALU(funcNum, rs, rtValue, rd, sh,
                                  programCounter)
                #registerFile[rd] = result
                rtype = f'{funcCode} ${rd}, ${rt}, {sh}\n'
                ALUCounter += 1
                print(
                    f'{rtype}PC = {programCounter} Instruction Count:{TotalInstructionCounter}'
                )
                print(
                    f'Before {value}: ${rd} = {registerFile[rd]}')
                registerFile[rd] = result
                print(f'After {value}: ${rd} = {registerFile[rd]}')
                print(
                    '-------------------------------------------')

              elif (funcNum == 1):
                  rs = int(instr[6:11], 2)
                  rt = int(instr[11:16], 2)
                  rd = int(instr[16:21], 2)
                  sh = 0

                  for registerKey, registerValue in registerFile.items(
                  ):
                      if rt == registerKey:
                          rtValue = registerValue

                  for registerKey, registerValue in registerFile.items(
                  ):
                      if rs == registerKey:
                          rsValue = registerValue

                  result = funcALU(funcNum, rsValue, rtValue, rd, sh,
                                    programCounter)
                  print

                  rtype = f'{funcCode} ${rd}, ${rs}, ${rt}\n'
                  SpecialCounter += 1
                  print(
                      f'{rtype}PC = {programCounter} Instruction Count:{TotalInstructionCounter}'
                  )
                  print(
                      f'Before {funcCode}: ${rd} = {registerFile[rd]}'
                  )
                  registerFile[rd] = result
                  print(
                      f'After {funcCode}: ${rd} = {registerFile[rd]}'
                  )
                  print(
                      '-------------------------------------------')
              else:
                  rs = int(instr[6:11], 2)
                  rt = int(instr[11:16], 2)
                  rd = int(instr[16:21], 2)
                  sh = 0
                  for registerKey, registerValue in registerFile.items(
                  ):
                      if rt == registerKey:
                          rtValue = registerValue
                  for registerKey, registerValue in registerFile.items(
                  ):
                      if rs == registerKey:
                          rsValue = registerValue

                  if (funcNum == 42):
                      OtherCounter += 1
                  else:
                      ALUCounter += 1
                  result = funcALU(funcNum, rsValue, rtValue, rd, sh,
                                    programCounter)

                  rtype = f'{funcCode} ${rd}, ${rs}, ${rt}\n'
                  print(
                      f'{rtype}PC = {programCounter} Instruction Count:{TotalInstructionCounter}'
                  )
                  print(
                      f'Before {funcCode}: ${rd} = {registerFile[rd]}'
                  )
                  registerFile[rd] = result
                  print(
                      f'After {funcCode}: ${rd} = {registerFile[rd]}'
                  )
                  print(
                      '-------------------------------------------')
        elif (key == 35 or key == 43):
            rs = int(instr[6:11], 2)
            rt = int(instr[11:16], 2)
            immBinary = instr[16:32]

            if int(immBinary[0] == '1'):
                immValue = twosCompliment(int(immBinary, 2),
                                          len(immBinary))
            else:
                immValue = int(immBinary, 2)
            
            if (key == 35):

                for registerKey, registerValue in registerFile.items():
                    if rs == registerKey:
                        rsValue = registerValue

                result = immALU(key, rsValue, rt, immValue, programCounter)
                
                if(cacheConfig == "1"):
                  DM(N, S, B, rsValue, result)
                elif(cacheConfig == "2"):
                  FA(N, S, B, rsValue, result)
                elif(cacheConfig == "3"):
                  config3(N,S,B,rsValue, result)
                elif(cacheConfig == "4"):
                  config4(N, S, B, rsValue, result)

                  
                # #------------------------------------------------------------------
                MemoryCounter += 1
                Itype = f'{value} ${rt}, {immValue}(${rs})\n'
                print(
                    f'{Itype}PC = {programCounter} Instruction Count:{TotalInstructionCounter}'
                )
                print(f'Before {value}: ${rt}:{registerFile[rt]}')
                registerFile[rt] = result
                print(f'After {value}: ${rt}:{registerFile[rt]}')
                print('-------------------------------------------')
            else:
                for registerKey, registerValue in registerFile.items():
                    if rt == registerKey:
                        rtValue = registerValue
                for registerKey, registerValue in registerFile.items():
                    if rs == registerKey:
                        rsValue = registerValue
                storeLocation = immValue + rsValue
                  #------------------------------------------------------------------
                if(cacheConfig == '1'):
                  DM(N, S, B, storeLocation, rtValue)
                elif(cacheConfig == "2"):
                  FA(N, S, B, storeLocation, rtValue)
                elif(cacheConfig == "3"):
                  config3(N, S, B, storeLocation, rtValue)
                elif(cacheConfig == "4"):
                  config4(N, S, B, storeLocation, rtValue)

                #------------------------------------------------------------------
                MemoryCounter += 1
                Itype = f'{value} ${rt}, {immValue}(${rs})\n'
                print(
                    f'{Itype}PC = {programCounter} Instruction Count:{TotalInstructionCounter}'
                )
                print(
                    f'Before {value}: DM{storeLocation}:{memory[storeLocation]}'
                )
                memory[storeLocation] = rtValue
                print(
                    f'After {value}: DM{storeLocation}:{memory[storeLocation]}'
                )
                print('-------------------------------------------')
        elif (key == 2):
            rs = rt = 0
            immBinary = instr[6:32]
            immBinary += '00'
            immValue = (int(immBinary, 2))
            newpc = immALU(key, rs, rt, immValue, programCounter)
            jumplabel = f'm{jcounter}'
            jcounter2 = f'm{jcounter}:\n'
            Itype = f'{value} {jumplabel}\n'
            JumpCounter += 1
            print(
                f'{Itype}PC = {programCounter} Instruction Count:{TotalInstructionCounter}'
            )
            print(f'Before {value}: PC = {programCounter}')
            print(f'After {value}: PC = {newpc}')
            print('-------------------------------------------')
            counter = 0
            for i in assemblyInstructions:
                if (key != i):
                    counter += 1
                else:
                    break
            #print(f'jump is :{immValue/4}')
            if Itype in assemblyInstructions:
                j = ((int(newpc / 4) + jcounter))
                print(f'jump is :{j}')
                assemblyInstructions.insert(j, jcounter2)

            jcounter += 1
            #pcTracker.append(newpc)
        elif (key == 4 or key == 5):
            rt = int(instr[6:11], 2)
            rs = int(instr[11:16], 2)
            immBinary = instr[16:32]

            if int(immBinary[0] == '1'):
                immValue = twosCompliment(int(immBinary, 2),
                                          len(immBinary))
            else:
                immValue = int(immBinary, 2)

            for registerKey, registerValue in registerFile.items():
                if rt == registerKey:
                    rtValue = registerValue
            for registerKey, registerValue in registerFile.items():
                if rs == registerKey:
                    rsValue = registerValue

            newpc = immALU(key, rsValue, rtValue, immValue, programCounter)
            loop = f'B{loopcounter}'
            loop2 = f'B{loopcounter}:\n'
            Itype = f'{value} ${rt}, ${rs}, {loop}\n'
            print(
                f'{Itype}PC = {programCounter} Instruction Count:{TotalInstructionCounter}'
            )
            print(f'Before {value}: PC = {programCounter}')
            print(f'After {value}: PC = {newpc}')
            print('-------------------------------------------')
            BranchCounter += 1

            if ((newpc not in pcTracker)):
                p = ((int(newpc / 4) + loopcounter))
                assemblyInstructions.insert(p, loop2)
                loopcounter += 1
                pcTracker.append(newpc)
        elif (key == 15):
            rs = 0
            rt = int(instr[11:16], 2)
            immBinary = instr[16:32]

            if int(immBinary[0] == '1'):
                immValue = twosCompliment(int(immBinary, 2),
                                          len(immBinary))
            else:
                immValue = int(immBinary, 2)

            ALUCounter += 1
            result = immALU(key, rs, rt, immValue, programCounter)
            Itype = f'{value} ${rt}, {immValue}\n'
            print(
                f'{Itype}PC = {programCounter} Instruction Count:{TotalInstructionCounter}'
            )
            print(f'Before {value}: ${rt} = {registerFile[rt]}')
            registerFile[rt] = result
            print(f'After {value}: ${rt} = {registerFile[rt]}')
            print('-------------------------------------------')

        else:
            ALUCounter += 1
            rs = int(instr[6:11], 2)
            rt = int(instr[11:16], 2)
            immBinary = instr[16:32]

            if (key == 13):
                immValue = int(immBinary, 2)
            else:
                if int(immBinary[0] == '1'):
                    immValue = twosCompliment(int(immBinary, 2),
                                              len(immBinary))
                else:
                    immValue = int(immBinary, 2)

            for registerKey, registerValue in registerFile.items():
                if rs == registerKey:
                    rsValue = registerValue

            result = immALU(key, rsValue, rt, immValue, programCounter)
            Itype = f'{value} ${rt}, ${rs}, {immValue}\n'
            print(
                f'{Itype}PC = {programCounter} Instruction Count:{TotalInstructionCounter}'
            )
            print(f'Before {value}: ${rt} = {registerFile[rt]}')
            registerFile[rt] = result
            print(f'After {value}: ${rt} = {registerFile[rt]}')
            print('-------------------------------------------')

    return newpc


def binarytoinstr(binaryInstruct):
    global loopcounter1
    global jcounter2
    global loopcounter
    global jcounter

    instr = binaryInstruct

    for key, value in opcodes.items():
        if int(instr[0:6], 2) == key:
            if key == 0:
                for funcNum, funcCode in functionCodes.items():
                    if int(instr[26:32], 2) == funcNum:
                        if funcNum == 0 or funcNum == 2 or funcNum == 3:
                            rs = 0
                            rt = int(instr[11:16], 2)
                            rd = int(instr[16:21], 2)
                            sh = int(instr[21:26], 2)

                            rtype = f'{funcCode} ${rd}, ${rt}, {sh}\n'
                        elif (funcNum == 1):
                            rs = int(instr[6:11], 2)
                            rt = int(instr[11:16], 2)
                            rd = int(instr[16:21], 2)
                            sh = 0

                            rtype = f'{funcCode} ${rd}, ${rs}, ${rt}\n'
                        else:
                            rs = int(instr[6:11], 2)
                            rt = int(instr[11:16], 2)
                            rd = int(instr[16:21], 2)
                            sh = 0

                            rtype = f'{funcCode} ${rd}, ${rs}, ${rt}\n'
                        assemblyInstructions.append(rtype)
            elif (key == 35 or key == 43):
                rs = int(instr[6:11], 2)
                rt = int(instr[11:16], 2)
                immBinary = instr[16:32]

                if int(immBinary[0] == '1'):
                    immValue = twosCompliment(int(immBinary, 2),
                                              len(immBinary))
                else:
                    immValue = int(immBinary, 2)

                Itype = f'{value} ${rt}, {immValue}(${rs})\n'
                assemblyInstructions.append(Itype)
            elif (key == 2):
                rs = rt = 0
                immBinary = instr[6:32]
                immBinary += '00'
                immValue = (int(immBinary, 2))
                jumplabel = f'm{jcounter2}'
                Itype = f'{value} {jumplabel}\n'

                assemblyInstructions.append(Itype)
                jcounter2 += 1
            elif (key == 4 or key == 5):
                rt = int(instr[6:11], 2)
                rs = int(instr[11:16], 2)
                immBinary = instr[16:32]

                if int(immBinary[0] == '1'):
                    immValue = twosCompliment(int(immBinary, 2),
                                              len(immBinary))
                else:
                    immValue = int(immBinary, 2)

                loop = f'B{loopcounter1}'
                Itype = f'{value} ${rt}, ${rs}, {loop}\n'

                assemblyInstructions.append(Itype)
                loopcounter1 += 1
            elif (key == 15):
                rs = 0
                rt = int(instr[11:16], 2)
                immBinary = instr[16:32]

                if int(immBinary[0] == '1'):
                    immValue = twosCompliment(int(immBinary, 2),
                                              len(immBinary))
                else:
                    immValue = int(immBinary, 2)

                Itype = f'{value} ${rt}, {immValue}\n'

                assemblyInstructions.append(Itype)
            else:
                rs = int(instr[6:11], 2)
                rt = int(instr[11:16], 2)
                immBinary = instr[16:32]

                if (key == 13):
                    immValue = int(immBinary, 2)
                else:
                    if int(immBinary[0] == '1'):
                        immValue = twosCompliment(int(immBinary, 2),
                                                  len(immBinary))
                    else:
                        immValue = int(immBinary, 2)

                Itype = f'{value} ${rt}, ${rs}, {immValue}\n'

                assemblyInstructions.append(Itype)


def assumbely_file():
    l = open('instr.asm')
    lines1 = l.readlines()
    l.close()

    instr_dict = {}
    label_dict = {}

    PC = 0
    for ln in lines1:
        pos = ln.find(":")
        if pos >= 0:
            label_dict[ln[:-2]] = PC
            continue
        instr_dict[PC] = ln[:-1]
        PC += 4

    print('\nBelow are all the instructions:')

    for PC, instr1 in instr_dict.items():
        print(f'{PC}: {instr1}')

    print('\nBelow are all the labels:')
    for label, PC in label_dict.items():
        print(f'{label} =  {PC} -> {instr_dict[PC]}')


#main

pcTracker = []
binList = generateBinaryInst()
instrDict = memoryInstruction(binList)
assemblyInstructions = []
logfile = []
inputfile = open('log.txt', 'w')
i = open('instr.asm', 'w')

for o, binarynumber in instrDict.items():
    binarytoinstr(binarynumber)

stepByStep = input(
    'Press 1 for non-stop mode or press 2 for step-by-step mode:\n')
cacheConfig = input(
  'Press 1 for direct mapping configuration\nPress 2 for 8-way FA configuration:\nPress 3 for a 2-way 4-set, SA configuration, block size of 16 Bits\nPress 4 for a 4-way 2-set, SA configuration, block size of 16 Bits:\n'
)

print(f'\nYou have choice CacheConfiguration {cacheConfig}\n')
input(f'Press Enter to start CacheConfiguration {cacheConfig}\n')

if(cacheConfig == "1"):
  N = 1
  S = 8
  B = 16
  logfile.append(f'---------------------Welcome to Direct Mapping CacheConfiguration-------------------------- \n\n------------------------------Where N = {N}, S = {S}, B = {B}-----------------------------------\n\n')
elif(cacheConfig == "2"):
  N = 8
  S = 1
  B = 16
  logfile.append(f'--------------------------Welcome to Fully Associative CacheConfiguration-------------------------- \n\n-------------------------------------Where N = {N}, S = {S}, B = {B}------------------------------------\n\n')
elif(cacheConfig == "3"):
  N = 2
  S = 4
  B = 16
  logfile.append(f'--------------------------Welcome to Set Associative CacheConfiguration-------------------------- \n\n-------------------------------------Where N = {N}, S = {S}, B = {B}------------------------------------\n\n')
elif(cacheConfig == "4"):
  N = 4
  S = 2
  B = 16
  logfile.append(f'--------------------------Welcome to Set Associative CacheConfiguration-------------------------- \n\n-------------------------------------Where N = {N}, S = {S}, B = {B}------------------------------------\n\n')

print('')
if stepByStep == '1':
    print('Welcome to non-stop mode\n')
    print('')
else:
    print('Welcome to step-by-step mode\n')
    print('')
    input('Press Enter to continue...')
programCounter = 0
EOF = len(binList) * 4
while (programCounter < EOF):
    for o, binaryvalue in instrDict.items():
        if (o == programCounter):
            programCounter = prog_file(binaryvalue, programCounter)
            programCounter += 4
            registerFile['PC'] = programCounter
            TotalInstructionCounter = ALUCounter + JumpCounter + BranchCounter + MemoryCounter + OtherCounter + SpecialCounter
            if stepByStep == '2':
                input('Press Enter to continue...')

            #print(f'Instruction Count:{TotalInstructionCounter}')

for y in assemblyInstructions:
  i.write(y)
i.close()
#assumbely_file()
print('')
printResults(registerFile, memory)
hitRate = int((Hit / (Hit+ Miss))*100)
logfile.append(f'Final HitRate is: {hitRate}%')

for z in logfile:
  inputfile.write(z)
inputfile.close()