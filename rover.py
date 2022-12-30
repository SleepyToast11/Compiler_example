import pathlib
import random
import sys
import time
import traceback

# The maximum amount of time that the rover can run in seconds
MAX_RUNTIME = 36000

NORTH=1
EAST=2
SOUTH=3
WEST=4 
robot='R'



# Rovers that exist
ROVER_1 = "Rover"
ROVERS = [
    ROVER_1
]

# Command file is stored within the rover directory. Here we're building one file
# for each of the rovers defined above
ROVER_COMMAND_FILES = {
    rover_name: pathlib.Path(pathlib.Path(__file__).parent.resolve(), f"{rover_name}.txt")
    for rover_name in ROVERS
}
for _, file in ROVER_COMMAND_FILES.items():
    with file.open("w") as f:
        pass

# Constant used to store the rover command for parsing
ROVER_COMMAND = {
    rover_name: None
    for rover_name in ROVERS
}


def get_command(rover_name):
    """Checks, and gets a command from a rovers command file.

    It returns True when something was found, and False
    when nothing was found. It also truncates the contents
    of the file if it found something so that it doesn't
    run the same command again (unless it was re-run from
    the controller/main program).
    """
    fcontent = None
    with ROVER_COMMAND_FILES[rover_name].open() as f:
        fcontent = f.read()
    if fcontent is not None and fcontent:
        ROVER_COMMAND[rover_name] = fcontent
        with ROVER_COMMAND_FILES[rover_name].open("w+") as f:
            pass
        return True
    return False


class Rover():
    def __init__(self, name, the_map):
        self._map = the_map
        self.ground_memo = the_map.copy()
        self.name = name
        self.x, self.y = self.spawn()
        self.orientation=NORTH

    def print(self, msg):
        print(f"{self.name}: {msg}")

    def parse_and_execute_cmd(self, command):
        self.print(f"Running command: {command}")
        pass

    def wait_for_command(self):
        start = time.time()
        while (time.time() - start) < MAX_RUNTIME:
            # Sleep 1 second before trying to check for
            # content again
            self.print("Waiting for command...")
            time.sleep(1)
            if get_command(self.name):
                self.print("Found a command...")
                try:
                    self.parse_and_execute_cmd(ROVER_COMMAND[self.name])
                except Exception as e:
                    self.print(f"Failed to run command: {ROVER_COMMAND[self.name]}")
                    self.print(traceback.format_exc())
                finally:
                    self.print("Finished running command.\n\n")
    
    def spawn(self):
      # Find an empty spot on the map to spawn the robot
      self.x, self.y=0,0
      found = False
      while not found:
        self.x = random.randint(0, len(self._map) - 1)
        self.y = random.randint(0, len(self._map[0]) - 1)
        if self._map [self.x][self.y] == ' ':
          found = True

      # Set the robot's starting position
      self._map [self.x][self.y] = 'S'
      return self.x,self.y
      
    
    def go_up(self):
      canTurn = self.can_go_up()
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
    
    def go_down(self):
      canTurn = self.can_go_left()
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
    
    def go_left(self):
      canTurn = self.can_go_left()
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
    
    def go_right(self):
      canTurn = self.can_go_right()
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
      if self._map[self.x-1][self.y] == 'D':
        print("digging.............")  
        self._map[self.x-1][self.y] = 'T'
        print("treasure was taken")
      elif self._map[self.x+1][self.y] == 'D':
        print("digging.............")  
        self._map[self.x+1][self.y] = 'T'
        print("treasure was taken")
      elif self._map[self.x][self.y+1] == 'D':
        print("digging.............")  
        self._map[self.x][self.y+1] = 'T'
        print("treasure was taken") 
      elif self._map[self.x][self.y-1] == 'D':
        print("digging.............")  
        self._map[self.x][self.y-1] = 'T'
        print("treasure was taken")         
      else:
          print("you can't dig here")
    
    def info(self):
      for i in range(len(self._map)):
       for j in range(len(self._map[i])):
        if self._map [i][j] == 'R':
          self._map [i][j] = ''
      
      self._map [self.x][self.y]=robot
      for row in self._map :
          print(''.join(row))
      print("the orientation is: ")
      if self.orientation==1:
          print("NORTH")
      if self.orientation==2:
          print("EAST")
      if self.orientation==3:
          print("SOUTH")
      if self.orientation==4:
          print("WEST")
      
      return self.x, self.y

    def can_go_right(self):
        canTurn = False
        if self.orientation==NORTH:          
            if self.x > 0 and self._map[self.x][self.y+1] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
                GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation==EAST:
            if self.x > 0 and self._map[self.x+1][self.y] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation == SOUTH:
            if self.x > 0 and self._map[self.x][self.y-1] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation==WEST:
            if self.x > 0 and self._map[self.x-1][self.y] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        return canTurn
    
    def can_go_left(self):
        canTurn = False
        if self.orientation==NORTH:          
         if self.x > 0 and self._map[self.x][self.y-1] != 'X':
             canTurn = True
             GLOBAL_SCOPE["systemBool"]["value"] = True
         else:
            GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation==EAST:
            if self.x > 0 and self._map[self.x-1][self.y] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation==SOUTH:
            if self.x > 0 and self._map[self.x][self.y+1] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation==WEST:
            if self.x > 0 and self._map[self.x+1][self.y] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        return canTurn

    def can_go_up(self):
        canTurn = False
        if self.orientation==NORTH:          
         if self.x > 0 and self._map[self.x-1][self.y] != 'X':
             canTurn = True
             GLOBAL_SCOPE["systemBool"]["value"] = True
         else:
            GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation==EAST:
            if self.x > 0 and self._map[self.x][self.y+1] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation==SOUTH:
            if self.x > 0 and self._map[self.x+1][self.y] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation==WEST:
            if self.x > 0 and self._map[self.x][self.y-1] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        return canTurn

    def can_go_down(self):
        canTurn = False
        if self.orientation==NORTH:          
         if self.x > 0 and self._map[self.x+1][self.y] != 'X':
             canTurn = True
             GLOBAL_SCOPE["systemBool"]["value"] = True
         else:
            GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation==EAST:
            if self.x > 0 and self._map[self.x][self.y-1] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation==SOUTH:
            if self.x > 0 and self._map[self.x-1][self.y] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        elif self.orientation==WEST:
            if self.x > 0 and self._map[self.x][self.y+1] != 'X':
                canTurn = True
                GLOBAL_SCOPE["systemBool"]["value"] = True
            else:
               GLOBAL_SCOPE["systemBool"]["value"] = False
        return canTurn

    def turn_right(self):
        
      if self.orientation == NORTH:
        self.orientation = EAST
      elif self.orientation == WEST:
        self.orientation = NORTH
      elif self.orientation == SOUTH:
        self.orientation = WEST
      elif self.orientation == EAST:
        self.orientation = SOUTH

    def turn_left(self):
        
      if self.orientation == NORTH:
        self.orientation = WEST
      elif self.orientation == EAST:
        self.orientation = NORTH
      elif self.orientation == SOUTH:
        self.orientation = EAST
      elif self.orientation == WEST:
        self.orientation = SOUTH


    def set_ground(self):

        self.ground_memo[self.x][self.y] = GLOBAL_SCOPE["systemInt"]["value"]

    def print_ground(self):
        
        print("ground were set at", self.ground_memo)

    def get_ground(self):

        GLOBAL_SCOPE["systemInt"]["value"] = self.ground_memo[self.x][self.y]

rover = Rover("", [])
def main():
    # Initialize the rovers
    if len(sys.argv) < 1:
        raise Exception("Missing file path to parse.")

    my_map = []
    filepath = pathlib.Path(sys.argv[1])
    with filepath.open() as f:
        my_map = f.readlines()
        ground_memo = f.readlines()

    global rover
    rover = Rover(ROVER_1, my_map)

    rover.wait_for_command()




if __name__=="__main__":
    main()

GLOBAL_SCOPE = {
    "rover": {"value": None, "type": "rover"}
    , "systemInt": {"value": 0, "type": "int"}
    , "systemBool": {"value": False, "type": "bool"}
    , "goRight": {"value": rover.go_right(), "type": "rover"}
    , "goUp": {"value": rover.go_up(), "type": "rover"}
    , "goLeft": {"value": rover.go_left(), "type": "rover"}
    , "goDown": {"value": rover.go_down(), "type": "rover"}
    , "canGoRight": {"value": rover.can_go_right(), "type": "rover"}
    , "canGoUp": {"value": rover.can_go_up(), "type": "rover"}
    , "canGoLeft": {"value": rover.can_go_left(), "type": "rover"}
    , "canGoDown": {"value": rover.can_go_down(), "type": "rover"}
    , "getGround": {"value": rover.get_ground(), "type": "rover"}
    , "setGround": {"value": rover.set_ground(), "type": "rover"}
    , "dig": {"value": rover.dig(), "type": "rover"}
    , "turnRight": {"value": rover.turn_right(), "type": "rover"}
    , "turnLeft": {"value": rover.turn_left(), "type": "rover"}
}