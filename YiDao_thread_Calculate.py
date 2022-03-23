import sys
import xlrd
import xlwt
import time
import copy
import psutil
import socket
import getopt
import warnings
import numpy

import YiDao_Constants as yc
from YiDao_Analyzer import Chessboard
from YiDao_Analyzer import Move
from YiDao_Chessmove import movechess
from YiDao_History import History

from YiDao_thread_UI import *


def runYiDao(ChessBoard):  ##  轮到AI走执行


  ChessBoard.rate()
  
  ChessBoard.showInfo(simplify=False)
  
  totalHistory = History(ChessBoard)  #  生成一个 History 类
  getResult = totalHistory.alphabeta(basetimes = ChessBoard.playtimes)  #  计算
  del totalHistory
  
  print("Ai返回的值",getResult)
  ChessBoard = movechess(ChessBoard,getResult,generate = True)
  
  return ChessBoard


def wait_for_player(Window,ChessBoard):  ##  轮到玩家走执行

  tmpSkip = False
  while not tmpSkip:
  
    time.sleep(0.5)  #  防止UI卡，每0.5秒检测一次
    tmpReturn = Window.checkChooseChess()
    tmpMove = tmpReturn[1]
    tmpSkip = tmpReturn[0]
  

  getMove = Move(int(tmpMove[0]),int(tmpMove[1]),int(tmpMove[2]),int(tmpMove[3]))
  ChessBoard = movechess(ChessBoard,getMove,generate = True)
  
  return ChessBoard

def initChessboardUI(Window,ChessBoard):  ##  更新UI上的棋盘

  for x in range(0,9,1):
    for y in range(0,10,1):
      Window.setChess(x,y,True,ChessBoard.data_board[x][y])
  

def calculate(Window):  ##  进行游戏的主循环

  ChessBoard = Chessboard(yc.init_chessboard,playtimes = 0)  #  初始化棋盘
  for x in range(9):
    for y in range(10):
      ChessBoard.generateMove(x,y)
  
  while True :

    initChessboardUI(Window, ChessBoard)  #  更新UI上的棋盘
    #  先看看开局库上有没有
    opening = ChessBoard.isInOpening()
    if opening[0]:  #  有，返回了一个 x y x y 的 List
      print("在开局库上找到了合适的棋盘")
      tmp = opening[1]
      ChessBoard = movechess(ChessBoard,Move(tmp[0],tmp[1],tmp[2],tmp[3]),generate = True)
    else:  #  没有，乖乖 alpha-beta
      ChessBoard = runYiDao(ChessBoard)
    
    initChessboardUI(Window, ChessBoard)
    ChessBoard = wait_for_player(Window, ChessBoard)


