
'''  移动棋子，产生新的棋盘  '''

import numpy
from YiDao_Analyzer import Chessboard

def movechess(Board, Move, generate = False) :

  #  把棋盘拉成线
  new_board = numpy.array(Board.data_board.reshape([90]))
  
  from_x = Move.from_x
  from_y = Move.from_y
  to_x = Move.to_x
  to_y = Move.to_y
  
  belong = Board.belong
  playtimes = Board.playtimes + 1
  
  #  移动棋子
  new_board[to_x * 10 + to_y] = int(new_board[from_x * 10 + from_y])
  new_board[from_x * 10 + from_y] = 0
  
  new_board_object = Chessboard(new_board,playtimes = playtimes,notes = Move.notes)
  
  #  直接生成信息
  if generate:

    for x in range(9):
      for y in range(10):

        new_board_object.generateMove(x,y)
    
  
  return new_board_object
