# -*- coding: utf-8 -*-
"""
Final work is in this Robot
"""

import random



ground_memo = []
NORTH=1
EAST=2
SOUTH=3
WEST=4 
rover='R'

class Robot:

  
  def __init__(self, map):
    self.map = map
    self.x, self.y = self.spawn()
    self.orientation=NORTH
  
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
    map[self.x][self.y] = 'S'
    return self.x,self.y
    
  
  def move_forward(self):
    canTurn = self.can_move_forward()
    if canTurn==True:
      if self.orientation==NORTH:  
          self.x -= 1
      elif self.orientation==EAST:
          self.y += 1
      elif self.orientation==SOUTH:
          self.x += 1
      elif self.orientation==WEST:
          self.y -= 1
    else:
        print("can't move")  
  
  def move_backward(self):
    canTurn = self.can_move_left()
    if canTurn==True:
      if self.orientation==NORTH:  
          self.x += 1
      elif self.orientation==EAST:
          self.y -= 1
      elif self.orientation==SOUTH:
          self.x -= 1
      elif self.orientation==WEST:
          self.y += 1
    else:
        print("can't move")  
  
  def move_left(self):
    canTurn = self.can_move_left()
    if canTurn==True:
      if self.orientation==NORTH:  
          self.y -= 1
      elif self.orientation==EAST:
          self.x -= 1
      elif self.orientation==SOUTH:
          self.y += 1
      elif self.orientation==WEST:
          self.x += 1
    else:
        print("can't move")  
  
  def move_right(self):
    canTurn = self.can_move_right()
    if canTurn==True:
      if self.orientation==NORTH:  
          self.y += 1
      elif self.orientation==EAST:
          self.x += 1
      elif self.orientation==SOUTH:
          self.y -= 1
      elif self.orientation==WEST:
          self.x -= 1
    else:
        print("can't move")  
      
  
  def dig(self):
    if self.map[self.x-1][self.y] == 'D':
      print("digging.............")  
      self.map[self.x-1][self.y] = 'T' 
      print("treasure was taken")
    elif self.map[self.x+1][self.y] == 'D':
      print("digging.............")  
      self.map[self.x+1][self.y] = 'T' 
      print("treasure was taken")
    elif self.map[self.x][self.y+1] == 'D':
      print("digging.............")  
      self.map[self.x][self.y+1] = 'T' 
      print("treasure was taken") 
    elif self.map[self.x][self.y-1] == 'D':
      print("digging.............")  
      self.map[self.x][self.y-1] = 'T' 
      print("treasure was taken")         
    else:
        print("you can't dig here")
  
  def info(self):
    for i in range(len(map)):
     for j in range(len(map[i])):
      if map[i][j] == 'R':
        map[i][j] = ''
    
    map[self.x][self.y]=rover
    for row in map:
        print(''.join(row))
    print("the orientation is ")
    if self.orientation==1:
        print("NORTH")
    if self.orientation==2:
        print("EAST")
    if self.orientation==3:
        print("SOUTH")
    if self.orientation==4:
        print("WEST")
    
    return self.x, self.y

  def can_move_right(self):
      canTurn = False
      if self.orientation==NORTH:          
       if self.x > 0 and self.map[self.x][self.y+1] != 'X':
           canTurn = True
           print("it can move")
       else:
          print("it can't move")
      elif self.orientation==EAST:
          if self.x > 0 and self.map[self.x+1][self.y] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      elif self.orientation==SOUTH:
          if self.x > 0 and self.map[self.x][self.y-1] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      elif self.orientation==WEST:
          if self.x > 0 and self.map[self.x-1][self.y] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      return canTurn
  
  def can_move_left(self):
      canTurn = False
      if self.orientation==NORTH:          
       if self.x > 0 and self.map[self.x][self.y-1] != 'X':
           canTurn = True
           print("it can move")
       else:
          print("it can't move")
      elif self.orientation==EAST:
          if self.x > 0 and self.map[self.x-1][self.y] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      elif self.orientation==SOUTH:
          if self.x > 0 and self.map[self.x][self.y+1] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      elif self.orientation==WEST:
          if self.x > 0 and self.map[self.x+1][self.y] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      return canTurn

  def can_move_forward(self):
      canTurn = False
      if self.orientation==NORTH:          
       if self.x > 0 and self.map[self.x-1][self.y] != 'X':
           canTurn = True
           print("it can move")
       else:
          print("it can't move")
      elif self.orientation==EAST:
          if self.x > 0 and self.map[self.x][self.y+1] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      elif self.orientation==SOUTH:
          if self.x > 0 and self.map[self.x+1][self.y] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      elif self.orientation==WEST:
          if self.x > 0 and self.map[self.x][self.y-1] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      return canTurn

  def can_move_backward(self):
      canTurn = False
      if self.orientation==NORTH:          
       if self.x > 0 and self.map[self.x+1][self.y] != 'X':
           canTurn = True
           print("it can move")
       else:
          print("it can't move")
      elif self.orientation==EAST:
          if self.x > 0 and self.map[self.x][self.y-1] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      elif self.orientation==SOUTH:
          if self.x > 0 and self.map[self.x-1][self.y] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      elif self.orientation==WEST:
          if self.x > 0 and self.map[self.x][self.y+1] != 'X':
              canTurn = True
              print("it can move")
          else:
             print("it can't move")
      return canTurn

  def rotate_right(self):
      
    if self.orientation == NORTH:
      self.orientation = EAST
    elif self.orientation == WEST:
      self.orientation = NORTH
    elif self.orientation == SOUTH:
      self.orientation = WEST
    elif self.orientation == EAST:
      self.orientation = SOUTH

  def rotate_left(self):
      
    if self.orientation == NORTH:
      self.orientation = WEST
    elif self.orientation == EAST:
      self.orientation = NORTH
    elif self.orientation == SOUTH:
      self.orientation = EAST
    elif self.orientation == WEST:
      self.orientation = SOUTH


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
#robot.dig()
#robot.move_forward()
#robot.move_left()
#robot.can_move_right()
#robot.move_right()
#robot.dig()
#robot.move_backward()
#robot.set_ground()
#robot.move_right()
#robot.dig()
#robot.set_ground()
#robot.get_ground()
robot.rotate_right()

robot.move_forward()
robot.move_right()
print(robot.info())

robot.rotate_left()
robot.move_backward()
print(robot.info())
robot.rotate_right()
print(robot.info())
robot.rotate_right()
robot.move_forward()
print(robot.info())
