# -*- coding: utf-8 -*-
"""
Final work is in this Robot
"""

import random

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
    if self.y > 0 and self.map[self.x][self.y-1] != 'X':
      self.y -= 1
      
  
  def move_backward(self):
    if self.y < len(self.map[0])-1 and self.map[self.x][self.y+1] != 'X':
      self.y += 1
      
  
  def move_left(self):
    if self.x > 0 and self.map[self.x-1][self.y] != 'X':
      self.x -= 1
      
  
  def move_right(self):
    if self.x < len(self.map)-1 and self.map[self.x+1][self.y] != 'X':
      self.x += 1
      
  
  def dig(self):
    if self.map[self.x][self.y] == 'D':
      self.map[self.x] = self.map[self.x][:self.y] + ' ' + self.map[self.x][self.y+1:]
  
  def info(self):
    return self.x, self.y


# Read map from a text file
with open('map.txt', 'r') as f:
  map = [list(line.strip()) for line in f]

# Create a robot and collect all the treasures on the map
robot = Robot(map)
while any('D' in row for row in map):
  robot.dig()
  robot.move_forward()
  robot.move_left()
  robot.move_right()
  robot.move_backward()
  print(robot.info())
  for row in map:
    print(''.join(row))
