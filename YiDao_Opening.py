
import os
import numpy
import copy

def decodeboard(ListBoard):

  dataDecodeall=[]
  newboard=[]
  cutboard=[]
  dataDecode=[]

  for objectLetter in list(ListBoard):
    tmpLetter=objectLetter
    if not tmpLetter.isdigit():
      tmpLetter=tmpLetter.replace('R','-1')
      tmpLetter=tmpLetter.replace('N','-2')
      tmpLetter=tmpLetter.replace('B','-3')
      tmpLetter=tmpLetter.replace('A','-4')
      tmpLetter=tmpLetter.replace('K','-5')
      tmpLetter=tmpLetter.replace('C','-6')
      tmpLetter=tmpLetter.replace('P','-7')
      tmpLetter=tmpLetter.replace('r','1')
      tmpLetter=tmpLetter.replace('n','2')
      tmpLetter=tmpLetter.replace('b','3')
      tmpLetter=tmpLetter.replace('a','4')
      tmpLetter=tmpLetter.replace('k','5')
      tmpLetter=tmpLetter.replace('c','6')
      tmpLetter=tmpLetter.replace('p','7')
      
      if not tmpLetter == "/" :

        dataDecode=dataDecode+[int(tmpLetter)]
      
    else:
    
      for index in range(int(tmpLetter)):
        dataDecode=dataDecode+[0]

  return dataDecode


def decodemove(tmpLetter):
 
    if not tmpLetter.isdigit():
      tmpLetter=tmpLetter.replace('a','0')
      tmpLetter=tmpLetter.replace('b','1')
      tmpLetter=tmpLetter.replace('c','2')
      tmpLetter=tmpLetter.replace('d','3')
      tmpLetter=tmpLetter.replace('e','4')
      tmpLetter=tmpLetter.replace('f','5')
      tmpLetter=tmpLetter.replace('g','6')
      tmpLetter=tmpLetter.replace('h','7')
      tmpLetter=tmpLetter.replace('i','8')
    else:
      tmpLetter=int(tmpLetter)
    
    
    return tmpLetter


def initopen():
  openingMoves = [[]]  #  初始化开局库


  with open("qf.txt", "r") as f:
    data = f.readlines()

  index = 0
  for eachLine in data:

    index += 1

    eachLine = eachLine.replace("\n","")
    cut_to_part = eachLine.split(" ")
    
    from_x = decodemove(cut_to_part[0][0])
    from_y = decodemove(cut_to_part[0][1])
    to_x = decodemove(cut_to_part[0][2])
    to_y = decodemove(cut_to_part[0][3])
    
    move = [int(from_x),int(from_y),int(to_x),int(to_y)]
    
    value = int(cut_to_part[1])
    board = copy.deepcopy(numpy.rot90(numpy.array(decodeboard( cut_to_part[2] ),dtype = "int8").reshape([10,9])))
    board = numpy.array(board,dtype = "int8").reshape([90])
    player = 0 if cut_to_part[3] == "w" else 1
    playtimes = (int(cut_to_part[7]) - 1 ) * 2 + player
    
    if index % 1000 == 0 :
      print("\r≡  正在加载开局库",100*index/len(data),"%                             ",end="")
      
    openingMoves += [[] for _ in range(playtimes- len(openingMoves) + 1)]  #  防止溢出
    openingMoves[playtimes].append([board.reshape([9,10]),move,value])
    
    #print(move,value,board.reshape([9,10]),player,playtimes)
  print("\r≡  正在加载开局库","完成                             ")
  
  return openingMoves


