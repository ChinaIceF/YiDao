
'''  分析器  '''

import numpy
import random
import YiDao_Constants as yc

class Move(object):
  
  def __init__(self, from_x, from_y, to_x, to_y, movetype = 0, score = 0, notes = ""):
    
    self.from_x = from_x
    self.from_y = from_y
    self.to_x = to_x
    self.to_y = to_y
    self.movetype = movetype #  0 是能吃子的  #  1 是仅能移动到但是不能吃（如炮的移动）
    self.score = score
    self.notes = notes


  def showInfo(self, simplify = False):
    
    if not simplify:
    
      print("↗  <Move> Detailed information:","\n")
      print("    from_x\t",self.from_x)
      print("    from_y\t",self.from_y)
      print("    to_x\t",self.to_x)
      print("    to_y\t",self.to_y)
      print("    notes\t",self.notes)
      
      #print("\n    score\t",self.score)
      print("")
  
    else:
      
      print("↗  <Move>       Simplified info:   ", "position:", self.from_x, self.from_y, self.to_x, self.to_y, "  notes:", self.notes)#, "  score:", self.score)
    
    return ""

  def __str__(self):
  
    self.showInfo()
    return ""



class Chessboard(object):
  
  def __init__(self, chessboardData, belong = -1, playtimes = 0, notes = ""):
    
    self.data_board = chessboardData.reshape([9,10])
    self.data_times = numpy.zeros([9,10],dtype = "int8")
    self.data_value = numpy.zeros([9,10],dtype = "int8")  #  计算步数的时候顺便生成了
    self.moves = []
    self.belong = belong
    self.playtimes = playtimes
    self.player = playtimes % 2
    self.notes = notes
    
    self.king = False
    self.value = 0

  def showInfo(self, simplify = False):
    
    if not simplify:
    
      print("□  <Chessboard> Detailed information:  ","\n")
      print("data_board:")
      print(self.data_board,"\n")
      print("data_times:")
      print(self.data_times,"\n")
      print("    moves\t",len(self.moves))
      print("    times_sum\t",numpy.sum(self.data_times),"\t( Equivalence )" if numpy.sum(self.data_times)==0 else "")
      print("    belong\t",self.belong,"\t( Undefined )" if self.belong==-1 else "\t( Targeted )")
      print("    playtimes\t",self.playtimes)
      print("    player\t",self.player,"\t(",yc.name_player[self.player],")")
      print("    notes\t",self.notes,"\t( Undefined )" if self.notes=="" else "")
      
      print("\n    value\t",self.value)
    
    else:
      
      print("□  <Chessboard> Simplified info:   ","times_sum:",numpy.sum(self.data_times),"  playtimes:",self.playtimes,"  notes:",self.notes,"  value:",self.value)
    
    return ""

  def __str__(self):
  
    self.showInfo()
    return ""

  def isEmpty(self, x, y):
    
    return self.data_board[x][y] == 0

  def isInOpening(self):
    
    if len(yc.openingMoves) - 1 >= self.playtimes :  #  如果不超过开局库
      
      choose = []
      for eachMove in yc.openingMoves[self.playtimes] :
        
        if (eachMove[0] == self.data_board).all()  == True :  #  如果地图一样
          choose.append(eachMove)
      

      if not choose == [] :  #  如果在开局库里找到了
        sum_weight = 0
        for tmp in choose:
          sum_weight += tmp[2]  #  总权重
        
        rdm = random.uniform(0, sum_weight)  #  生成 0 到 总权重 的一个随机数
        
        try_weight = 0
        for tmp in choose:
          try_weight += tmp[2]
          if try_weight >= rdm:  #  找到了选中的
            return [True,tmp[1]]
            
      else:  #  没找到
        return [False,None]


  def rate(self):
    
    #  如果被标记为被将军了，要减权
    if self.king:
      self.value -= 50
    
    ##  各种算法的权重
    power_mat = 0.2
    power_mox_score = 0.8
    
    #  简单的算法  3.22 决定
    #  times 与 data_board 两个矩阵点乘  得到的就是评分  暂不考虑别的
    
    matrix_data_times = self.data_times.reshape([1,90])
    matrix_data_board = self.data_board.reshape([90,1])
    self.value += numpy.dot(matrix_data_times,matrix_data_board)[0][0] * power_mat
    
    #  在所有走法里选出一个 走法评价函数最大值的走法
    #  公式：吃子子力 * ( 去点次数 * 是否不是将 + 1 ) + 去点点权 * 这个子的子力
    
    mox_score = -1000000
    for eachMove in self.moves :
      
      from_x = eachMove.from_x
      from_y = eachMove.from_y
      to_x = eachMove.to_x
      to_y = eachMove.to_y
      
      eachpoint_Pos = (to_x*10+to_y) * - ( self.player * 2 - 1 ) - self.player
      
      chessType_from = abs(self.data_board[from_x][from_y])
      chessType_to = abs(self.data_board[to_x][to_y])
      

      score = ( yc.value_chess[chessType_to] * ( self.data_times[to_x][to_y] * int( not chessType_to==5 ) + 1 ) + 
                    yc.value_eachpoint[chessType_from][eachpoint_Pos] * yc.value_movement[chessType_from] )
      
      if mox_score < score :
        mox_score = float(score)

    self.value += mox_score * power_mox_score
  
  '''
  def getValue(self):
    
    for eachMove in self.moves :
      
      from_x = eachMove.from_x
      from_y = eachMove.from_y
      to_x = eachMove.to_x
      to_y = eachMove.to_y
      
      eachpoint_Pos = (from_x*10+from_y) * - ( self.player * 2 - 1 ) - self.player
      
      chessType_from = abs(self.data_board[from_x][from_y])
      chessType_to = abs(self.data_board[to_x][to_y])
      

      score = ( yc.value_chess[chessType_to] * yc.value_eachpoint[chessType_from][eachpoint_Pos] +  #  目标子力 * 目标点权
                   self.data_times[to_x][to_y] +  #  目标次数
                   int(chessType_to == 0) * yc.value_movement[chessType_from] )  #  如果为空，加上偏置权
      eachMove.score = score
      self.value += score ** 3
      
    self.moves = merge_sort(self.moves)
    self.value /= len(self.moves)
    #self.value = self.moves[-1].score ** 2 - self.moves[0].score ** 2  #  最大最小方差
  '''


  def generateMove(self, x, y):
    
    ##  重写的生成走法
    
    self.data_value[x][y] = yc.value_chess[abs(self.data_board[x][y])]
    
    if not self.data_board[x][y] == 0 :  #  如果不是空位
    
      board = self.data_board
      moves = self.moves
      times = self.data_times
      codePlayer = 1 - 2 * self.player
      isMine = board[x][y] * codePlayer > 0    #如果不为空且是我的棋子   车1 马2 象3 士4 将5 炮6 兵7
      chessType = abs(board[x][y])
      chessOwner = int( board[x][y] > 0 ) * 2 - 1
      chessAddTo = codePlayer * chessOwner
      chessName = "{"+"type:"+yc.name_chess[chessType]+",owner:"+str(chessOwner)+"}"

      if    chessType == 1 :  #车
        
        for X in range(x+1,9,1):
          times[X][y] += chessAddTo
          if board[X][y] * codePlayer <= 0 and isMine:
            moves.append(Move(x, y, X, y, notes = chessName))
          if (board[X][y]!=0):
            break
            
        for X in range(x-1,-1,-1):
          times[X][y] += chessAddTo
          if board[X][y] * codePlayer <= 0 and isMine:
            moves.append(Move(x, y, X, y, notes = chessName))
          if (board[X][y]!=0):
            break

        for Y in range(y+1,10,1):
          times[x][Y] += chessAddTo
          if board[x][Y] * codePlayer <= 0 and isMine:
            moves.append(Move(x, y, x, Y, notes = chessName))
          if (board[x][Y]!=0):
            break

        for Y in range(y-1,-1,-1):
          times[x][Y] += chessAddTo
          if board[x][Y] * codePlayer <= 0 and isMine:
            moves.append(Move(x, y, x, Y, notes = chessName))
          if (board[x][Y]!=0):
            break

      elif chessType == 2:  #马
       
        #循环序列是一个数组
        #数组格式：[检测X,检测Y,[到X,到Y],[到X,到Y]]
        
        for XY in [[x+0,y+1,[x+1,y+2],[x-1,y+2]],
                         [x+0,y-1,[x+1,y-2],[x-1,y-2]],
                         [x+1,y+0,[x+2,y+1],[x+2,y-1]],
                         [x-1,y+0,[x-2,y+1],[x-2,y-1]]]:
                         

          if (0<=XY[2][0]<=8 and 0<=XY[2][1]<=9):
            if board[XY[0]][XY[1]] == 0:  #  如果不蹩脚
              times[XY[2][0]][XY[2][1]] += chessAddTo
              if board[XY[2][0]][XY[2][1]] * codePlayer <= 0 and isMine:
                moves.append(Move(x, y, XY[2][0], XY[2][1], notes = chessName))
                
          if (0<=XY[3][0]<=8 and 0<=XY[3][1]<=9):
            if board[XY[0]][XY[1]] == 0:  #  如果不蹩脚
              times[XY[3][0]][XY[3][1]] += chessAddTo
              if board[XY[3][0]][XY[3][1]] * codePlayer <= 0 and isMine:
                moves.append(Move(x, y, XY[3][0], XY[3][1], notes = chessName))

      elif chessType == 3:  #象
      
        #循环序列是一个数组
        #数组格式：[检测X,检测Y,到X,到Y]
        
        for XY in [[x+1,y+1,x+2,y+2],
                         [x+1,y-1,x+2,y-2],
                         [x-1,y+1,x-2,y+2],
                         [x-1,y-1,x-2,y-2]]:

          if 0 <= XY[2] <= 8 and 0 <= XY[3] <= 9 :
            if board[XY[0]][XY[1]] == 0 :
              if ( 0 <= XY[3] <= 4 and chessOwner == 1 ) or ( 5 <= XY[3] <= 9 and chessOwner == -1 ):
                times[XY[2]][XY[3]] += chessAddTo
                if board[XY[2]][XY[3]] * codePlayer <= 0 and isMine :
                  moves.append(Move(x, y, XY[2], XY[3], notes = chessName))

      elif chessType == 4:  #士
      
        #循环序列是一个数组
        #数组格式：[到X,到Y]
        #X方向的限制始终是在米字格内，即3-5
        
        for XY in [[x+1,y+1],[x+1,y-1],[x-1,y+1],[x-1,y-1]]:
          if 3 <= XY[0] <= 5 and (( 0 <= XY[1] <= 2 and chessOwner == 1 ) or ( 7 <= XY[1] <= 9 and chessOwner == -1 )):
            times[XY[0]][XY[1]] += chessAddTo
            if board[XY[0]][XY[1]] * codePlayer <= 0 and isMine :
              moves.append(Move(x, y, XY[0], XY[1], notes = chessName))

      elif chessType == 5:  #将
        
        #循环序列是一个数组
        #数组格式：[到X,到Y]
        #X方向的限制始终是在米字格内，即3-5
        #避免老将对老将   向对面进行直线检查
        
        for XY in [[x,y+1],[x,y-1],[x+1,y],[x-1,y]]:
          if 3 <= XY[0] <= 5 and (( 0 <= XY[1] <= 2 and chessOwner == 1 ) or ( 7 <= XY[1] <= 9 and chessOwner == -1 )):
            times[XY[0]][XY[1]] += chessAddTo
            if board[XY[0]][XY[1]] * codePlayer <= 0 and isMine :
              moves.append(Move(x, y, XY[0], XY[1], notes = chessName))

      elif chessType == 6:  #炮
      
        for X in range(x+1,9,1):
          if (board[X][y]*codePlayer==0):
            if isMine:
              moves.append(Move(x, y, X, y, notes = chessName))
          else:
            for _X in range(X+1,9,1):
              times[_X][y] += chessAddTo
              if board[_X][y] * codePlayer < 0 :
                if isMine:
                  moves.append(Move(x, y, _X, y, notes = chessName))
                break
              if board[_X][y] * codePlayer > 0 :
                break
            break

        for X in range(x-1,-1,-1):
          if (board[X][y]*codePlayer==0):
            if isMine:
              moves.append(Move(x, y, X, y, notes = chessName))
          else:
            for _X in range(X-1,-1,-1):
              times[_X][y] += chessAddTo
              if board[_X][y] * codePlayer < 0 :
                if isMine:
                  moves.append(Move(x, y, _X, y, notes = chessName))
                break
              if board[_X][y] * codePlayer > 0 :
                break
            break

        for Y in range(y+1,10,1):
          if (board[x][Y]*codePlayer==0):
            if isMine:
              moves.append(Move(x, y, x, Y, notes = chessName))
          else:
            for _Y in range(Y+1,10,1):
              times[x][_Y] += chessAddTo
              if board[x][_Y] * codePlayer < 0 :
                if isMine:
                  moves.append(Move(x, y, x, _Y, notes = chessName))
                break
              if board[x][_Y] * codePlayer > 0 :
                break
            break

        for Y in range(y-1,-1,-1):
          if (board[x][Y]*codePlayer==0):
            if isMine:
              moves.append(Move(x, y, x, Y, notes = chessName))
          else:
            for _Y in range(Y-1,-1,-1):
              times[x][_Y] += chessAddTo
              if board[x][_Y] * codePlayer < 0 :
                if isMine:
                  moves.append(Move(x, y, x, _Y, notes = chessName))
                break
              if board[x][_Y] * codePlayer > 0 :
                break
            break

      elif chessType == 7:  #兵
      
        #循环序列是一个数组
        #数组格式：[到X,到Y]
        
        tmpRule=[[5,9],[],[0,4]]
        tmpList=[]
        
        if 0 <= y <= 4 :
          if chessOwner == 1 :
            tmpList=[[x,y+1]]
          else:
            tmpList=[[x,y-1],[x+1,y],[x-1,y]]
        else:
          if chessOwner == 1 :
            tmpList=[[x,y+1],[x+1,y],[x-1,y]]
          else:
            tmpList=[[x,y-1]]
        
        for XY in tmpList:
          if (0<=XY[0]<=8 and 0<=XY[1]<=9):
            times[XY[0]][XY[1]] += chessAddTo
            if board[XY[0]][XY[1]] * codePlayer <= 0 and isMine :
              moves.append(Move(x, y, XY[0], XY[1], notes = chessName))








#归并算法排序权值
def merge(A, B):
    #取第一个元素作为值。返回的是一个集合的集合
    c = []
    h = j = 0
    while j < len(A) and h < len(B):
        if A[j].score < B[h].score:
            c.append(A[j])
            j += 1
        else:
            c.append(B[h])
            h += 1

    if j == len(A):
        for i in B[h:]:
            c.append(i)
    else:
        for i in A[j:]:
            c.append(i)

    return c
def merge_sort(lists):
    if len(lists) <= 1:
        return lists
    middle = len(lists)/2
    left = merge_sort(lists[:int(middle)])
    right = merge_sort(lists[int(middle):])
    return merge(left, right)