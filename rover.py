import multiprocessing
import pathlib
import time
import traceback
import random

# The maximum amount of time that the rover can run in seconds
MAX_RUNTIME = 36000

ground_memo = []
NORTH=1
EAST=2
SOUTH=3
WEST=4 
robot='R'



# Rovers that exist
ROVER_1 = "Rover1"
ROVER_2 = "Rover2"
ROVERS = [
    ROVER_1,
    ROVER_2,
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
    def __init__(self, name):
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
      
      map[self.x][self.y]=robot
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


def main():
    # Initialize the rovers
    rover1 = Rover(ROVER_1)
    rover2 = Rover(ROVER_2)
    my_rovers = [rover1, rover2]

    # Run the rovers in parallel
    procs = []
    for rover in my_rovers:
        p = multiprocessing.Process(target=rover.wait_for_command, args=())
        p.start()
        procs.append(p)

    # Wait for the rovers to stop running (after MAX_RUNTIME)
    for p in procs:
        p.join()


if __name__=="__main__":
    main()
