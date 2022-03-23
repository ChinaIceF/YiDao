
'''  常量  '''

import numpy
from YiDao_Opening import initopen

version = "New Format - beta 0.1"
database_version = "b 0.1"

openingMoves = initopen()  #  开局库

init_chessboard = numpy.array(  ##  初始棋盘
  [ 1, 0, 0, 7, 0,   0,-7, 0, 0,-1,
     2, 0, 6, 0, 0,   0, 0,-6, 0,-2,
     3, 0, 0, 7, 0,   0,-7, 0, 0,-3,
     4, 0, 0, 0, 0,   0, 0, 0, 0,-4,
     5, 0, 0, 7, 0,   0,-7, 0, 0,-5,
     4, 0, 0, 0, 0,   0, 0, 0, 0,-4,
     3, 0, 0, 7, 0,   0,-7, 0, 0,-3,
     2, 0, 6, 0, 0,   0, 0,-6, 0,-2,
     1, 0, 0, 7, 0,   0,-7, 0, 0,-1
  ] , dtype = "int8" )  #  这是初始状态的棋盘
'''
init_chessboard = numpy.array(
  [ 0, 0, 0, 7, 0,   0, -7, 0, 0, 0,
     0, 0, 0, 0, 0,   0, 0, 0, 0, 0,
     0, 0, 0, 7, 0,   0, -7, 0, 0, 0,
     0, 0, 0, 0, 0,   0, 0, 0, 0, 0,
     0, 0, 0, 7, 0,   0, -7, 0, 0, 0,
     0, 0, 0, 0, 0,   0, 0, 0, 0, 0,
     0, 0, 0, 7, 0,   0, -7, 0, 0, 0,
     0, 0, 0, 0, 0,   0, 0, 0, 0, 0,
     0, 0, 0, 7, 0,   0, -7, 0, 0, 0
  ] , dtype = "int8" )  #  这是初始状态的棋盘
  '''

value_eachpoint = [  ##  每个点，每一种棋对应的棋权
  
  numpy.array( [
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  ], dtype = "float64" ) ,  #  [0] 空

  numpy.array( [
      -6, 5, -2, 4, 8, 8, 6, 6, 6, 6,
      6, 8, 8, 9, 12, 11, 13, 8, 12, 8,
      4, 6, 4, 4, 12, 11, 13, 7, 9, 7,
      12, 12, 12, 12, 14, 14, 16, 14, 16, 13,
      0, 0, 12, 14, 15, 15, 16, 16, 33, 14,
      12, 12, 12, 12, 14, 14, 16, 14, 16, 13,
      4, 6, 4, 4, 12, 11, 13, 7, 9, 7,
      6, 8, 8, 9, 12, 11, 13, 8, 12, 8,
      -6, 5, -2, 4, 8, 8, 6, 6, 6, 6
  ], dtype = "float64" ) ,  #  [1] 车

  numpy.array( [
      0, -3, 5, 4, 2, 2, 5, 4, 2, 2,
      -3, 2, 4, 6, 10, 12, 20, 10, 8, 2,
      2, 4, 6, 10, 13, 11, 12, 11, 15, 2,
      0, 5, 7, 7, 14, 15, 19, 15, 9, 8,
      2, -10, 4, 10, 15, 16, 12, 11, 6, 2,
      0, 5, 7, 7, 14, 15, 19, 15, 9, 8,
      2, 4, 6, 10, 13, 11, 12, 11, 15, 2,
      -3, 2, 4, 6, 10, 12, 20, 10, 8, 2,
      0, -3, 5, 4, 2, 2, 5, 4, 2, 2
  ], dtype = "float64" ) ,  #  [2] 马

  numpy.array( [
      0, 0, -2, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, -2, 0, 0, 0, 0, 0, 0, 0
  ], dtype = "float64" ) ,  #  [3] 象

  numpy.array( [
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  ], dtype = "float64" ) ,  #  [4] 士

  numpy.array( [
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      1, -8, -9, 0, 0, 0, 0, 0, 0, 0,
      5, -8, -9, 0, 0, 0, 0, 0, 0, 0,
      1, -8, -9, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  ], dtype = "float64" ) ,  #  [5] 将

  numpy.array( [
      0, 0, 1, 0, -1, 0, 0, 1, 2, 4,
      0, 1, 0, 0, 0, 0, 3, 1, 2, 4,
      1, 2, 4, 0, 3, 0, 3, 0, 0, 0,
      3, 2, 3, 0, 0, 0, 2, -5, -4, -5,
      3, 2, 5, 0, 4, 4, 4, -4, -7, -6,
      3, 2, 3, 0, 0, 0, 2, -5, -4, -5,
      1, 2, 4, 0, 3, 0, 3, 0, 0, 0,
      0, 1, 0, 0, 0, 0, 3, 1, 2, 4,
      0, 0, 1, 0, -1, 0, 0, 1, 2, 4
  ], dtype = "float64" ) ,  #  [6] 炮

  numpy.array( [
      0, 0, 0, -2, 3, 10, 20, 20, 20, 0,
      0, 0, 0, 0, 0, 18, 27, 30, 30, 0,
      0, 0, 0, -2, 4, 22, 30, 45, 50, 0,
      0, 0, 0, 0, 0, 35, 40, 55, 65, 2,
      0, 0, 0, 6, 7, 40, 42, 55, 70, 4,
      0, 0, 0, 0, 0, 35, 40, 55, 65, 2,
      0, 0, 0, -2, 4, 22, 30, 45, 50, 0,
      0, 0, 0, 0, 0, 18, 27, 30, 30, 0,
      0, 0, 0, -2, 3, 10, 20, 20, 20, 0
  ], dtype = "float64" ) ,  #  [7] 卒

]  #  注意：这段数据暂时使用网上的资料，到后期记得更换。来自：
    #  https://blog.csdn.net/weixin_43398590/article/details/106321557?spm=1001.2101.3001.6650.9&utm_medium=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~Rate-9.pc_relevant_antiscanv2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~Rate-9.pc_relevant_antiscanv2&utm_relevant_index=14

value_chess = [   0, 500, 300, 250, 250,    0,   300,  80 ]  ##  每一种棋对应的棋权
#                      空     车     马     象     士     将     炮     兵

value_movement = [0, 6, 12, 1,  1,  0, 6, 15]  ##  移动偏置权
#                              空 车 马 象 士 将 炮 兵

name_chess = ["<空>","车","马","象","士","将","炮","兵"]
name_player = ["YiDaoAI","Player"]

depth_max = 4  ##  搜索的最深深度

value_max_limit = numpy.inf
value_min_limit = - numpy.inf  ##  正无穷与负无穷












