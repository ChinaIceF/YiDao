
'''  历史表，一棵很大很大很大的n叉树  '''

import numpy
import YiDao_Constants as yc
from YiDao_Chessmove import movechess

class History(object):

  def __init__(self, parent, input_children = [], alpha_beta = [yc.value_min_limit, yc.value_max_limit]):

    self.parent = parent  #  一个 Board 类
    self.children = input_children  #  以后会成为一个 History 类的 List
    #print(self.children)
    self.value = parent.value  #  方便比较而已
    
    self.alpha_beta = alpha_beta[:]

  def __str__(self):
    #self.parent.showInfo(simplify = False)
    return self.parent.notes

  def addchild(self, other):
  
    #  这里 other 应是一个 Board 类，这个方法自动处理成 History 类
    self.children.append(History(other,alpha_beta = self.alpha_beta))  #  给生成的子节点传入现有的 alpha beta


  def alphabeta(self,basetimes = 0):
  
    ##  注意，在开始 alpha-beta 剪枝算法前，这个棋盘的所有走法必须全部生成
    ##  即 self.moves 具有全面性
    
    #  玩家 0 记录 alpha （子节点最大值）
    #  玩家 1  记录 beta   （子节点最小值）
    #if self.parent.playtimes <= 2 :
    #print("＃",self.parent.playtimes,self.parent.playtimes*"\t","计算",self.alpha_beta,self.parent.player)
    tmpChildren = []
    
    truelevel = self.parent.playtimes - basetimes
    choose = None
    index = 0
    #print("＋",truelevel,truelevel*"\t","开启新层",self.alpha_beta)
   
    for eachmove in self.parent.moves:  #  遍历整个走法
    
      index += 1
      
      newBoard = movechess(self.parent, eachmove, generate = True)  #  根据走法之一创建新的 Board 类
      newBoard.rate()
      
      if truelevel + 1 < yc.depth_max:  #  如果没到指定深度
      #  self.addchild(newBoard)  #  添加到 self.children 里
        tmpChildren.append(History(newBoard,alpha_beta = self.alpha_beta))  #  给生成的子节点传入现有的 alpha beta
        tmpGetReturn = tmpChildren[-1].alphabeta(basetimes = basetimes)  #  往下搜 0 返回 alpha     1 返回 beta
        #print(self.alpha_beta)
        
        if tmpGetReturn[0] == "cut":  #  如果剪枝
          #self.children.pop()
          continue
        
        if tmpGetReturn[0] == True :
          if ((tmpGetReturn[1] > self.alpha_beta[0] and self.parent.player == 0) or 
               (tmpGetReturn[1] < self.alpha_beta[1] and self.parent.player == 1)): #  自己找最大

            #print("修改",self.alpha_beta,self.parent.player,tmpGetReturn[1])
            self.alpha_beta[self.parent.player] = tmpGetReturn[1]
            #return [True,tmpGetReturn[1]]    #  符合条件  0 改 alpha   1 改 beta
            #print("☆",truelevel,truelevel*"\t","值更新",self.alpha_beta)
            
            if self.parent.playtimes == basetimes : #  如果是一个根节点
              choose = eachmove
              #print("★",truelevel,truelevel*"\t","根节点更新",choose)

        #  要剪枝的情况：如果最小值大于等于最大值，就不用搜了
        
        if self.alpha_beta[0] >= self.alpha_beta[1] :
          print("－",truelevel,truelevel*"\t","剪枝",self.alpha_beta," 这一层还剩",len(self.parent.moves) - index)
          return ["cut",None]
        
      else :                              #  如果到了指定深度，直接返回这个棋盘的评分即可
        #self.children.pop()  #  删除刚刚的无用数据
        return [True,newBoard.value]  #  True 修改父节点的值

    #print("√",truelevel,truelevel*"\t","这一层已经遍历完成")

    
    if self.parent.playtimes == basetimes :  #  如果全部计算完了
      return choose
    return [True,self.alpha_beta[self.parent.player]]


  
  