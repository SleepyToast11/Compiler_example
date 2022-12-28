# -*- coding: utf-8 -*-
"""
Final work is in this Robot
"""

import random


ground_memo = []

class Robot:
  def __init__(self, map):
    self.map = map
    self.x, self.y = self.spawn()
  
  def spawn(self):
    # Find an empty spot on the map to spawn the robot
    self.x, self.y=0,0
    found = False
    while not found:
      self.x = random.randint(0, len(self.map) - 1)
      self.y = random.randint(0, len(self.map[0]) - 1)
      if map[self.x][self.y] == ' ':
        found = True

    # Set the robot's starting position
    map[self.x][self.y] = 'R'
    return self.x,self.y
    
  
  def move_forward(self):
    canTurn = self.can_move_forward()
    if canTurn==True:
      self.y -= 1
    else:
        print("can't move forward")  
  
  def move_backward(self):
     canTurn = self.can_move_left()
     if canTurn==True:
      self.y += 1
     else:
         print("can't move backwards") 
  
  def move_left(self):
    canTurn = self.can_move_left()
    if canTurn==True:
      self.x -= 1
    else:
        print("can't turn left") 
  
  def move_right(self):
    canTurn = self.can_move_right()
    if canTurn==True:
        self.x += 1
    else:
        print("can't turn right")
      
  
  def dig(self):
    if self.map[self.x][self.y] == 'D':
      print("digging.............")  
      self.map[self.x][self.y] = 'T' 
      print("treasure was taken")
    else:
        print("you can't dig here")
  
  def info(self):
    for row in map:
        print(''.join(row))
    return self.x, self.y

  def can_move_right(self):
      canTurn = False
      if self.x > 0 and self.map[self.x-1][self.y] != 'X':
          canTurn = True
          print("it can move")
      else:
          print("it can't move")
      return canTurn
  
  def can_move_left(self):
      canTurn = False
      if self.x < len(self.map)-1 and self.map[self.x+1][self.y] != 'X':
          canTurn = True
      return canTurn

  def can_move_forward(self):
      canTurn = False
      if self.y > 0 and self.map[self.x][self.y-1] != 'X':
          canTurn = True
      return canTurn

  def can_move_backward(self):
      canTurn = False
      if self.y < len(self.map[0])-1 and self.map[self.x][self.y+1] != 'X':
          canTurn = True
      return canTurn
    
  def set_ground(self):
      found=False
      i=0
      for i in range(len(ground_memo)):
          if [self.x,self.y]==ground_memo[i]:
              found=True
      if found==False:
          print("ground set at :" )
          print([self.x,self.y])
          ground_memo.append([self.x,self.y])
      else:
          print("it's already been set")
      
      return ground_memo

  def get_ground(self):
      
      print("ground were set at", ground_memo) 
    
# Read map from a text file
with open('map.txt', 'r') as f:
  map = [list(line.strip()) for line in f]

# Create a robot and collect all the treasures on the map
robot = Robot(map)

print(robot.info())
robot.dig()
#robot.move_forward()
#robot.move_left()
#robot.can_move_right()
robot.move_right()
robot.dig()
#robot.move_backward()
robot.set_ground()
robot.move_right()
robot.dig()
robot.set_ground()
robot.get_ground()


print(robot.info())
