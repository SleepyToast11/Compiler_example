import pathlib
import random
import sys
import time
import traceback

# The maximum amount of time that the rover can run in seconds
MAX_RUNTIME = 36000
CURRENT_SCOPE = {}
cursor = 0
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
    "Rover": None,
    "code": []
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
        ROVER_COMMAND["code"] = command.split()
        global cursor
        cursor = 0
        global CURRENT_SCOPE
        CURRENT_SCOPE = {}
        program = ProgramNode()
        program.parse()
        program.check_scope(None, None)
        program.check_semantics()
        program.run()


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
      self._map[self.x][self.y] = "S"
      return self.x, self.y
      
    
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

    # noinspection PyTypeChecker
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

    # noinspection PyTypeChecker
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




rover = None
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


class AbstractNode():
    scope = {}
    option = None

    def __init__(self):
        self.initial_cursor = cursor
        self.nodes = []

    def check_childs(self, index, ob_type, superType):
        return self.nodes[index].get_types(superType) == ob_type

    def get_type(self, ob_type):
        pass

    def get_child_type(self, index, ob_type):
        return self.nodes[index].get_type(ob_type)

    # generic run function for all nodes, most will not run and be called by other methods like get val or set value
    def run(self):
        for child in self.nodes:
            child.run()

    def check_semantics(self):
        for child in self.nodes:
            if child is not None:
                child.check_semantics()

    def get_Ids(self, list):
        for child in self.nodes:
            if child is not None:
                list = child.get_Ids(list)
        return list

    def name(self):
        return None

    def reset(self):
        global cursor
        cursor = self.initial_cursor
        return True

    def get_token(self):
        return ROVER_COMMAND["code"][cursor]

    def verify_and_add_token(self, index, my_node):
        val = my_node.parse()
        if val is None:
            return True
        elif val:
            self.nodes.append(my_node)
            return True
        else:
            return False

    def iterate_cursor(self):
        global cursor
        cursor += 1
        return True

    def verify_and_add_non_token_node(self, index, string):
        if self.get_token() is string:
            self.nodes.append(None)
            self.iterate_cursor()
            return True
        else:
            return False

    def check_scope(self, decl_list, assign_list):
        for child in self.nodes:
            if child is not None:
                decl_list, assign_list = child.check_scope(decl_list, assign_list)
        return decl_list, assign_list

    def parse(self):
        return True



class BasicNode(AbstractNode):
    basic = {"int", "bool", "double"}

    def name(self):
        return "BasicNode"

    def get_type(self, ob_type):
        return self.option

    def parse(self):
        token = self.get_token()
        if token in self.basic:
            # self.nodes.append(GenericNode(token))
            self.iterate_cursor()
            self.option = token
            return True
        else:
            return False












"""
Entering the nodes of the parser. We tried really hard to not make it only one file, we were thinking about 
having a second file that would be sent the parsing code, which then would be accessed, parsed, ran and 
when a rover token reached would sent it to the main rover file with a token to say its a command. for the 
two way communication, the rover would itself write and the code would block until the value is read. I started
implementing that, but it was really daunting and although quite in line with the project, calling it satellite
and making it as if the rover communicated through a satellite which does the brunt of the work and only sending
the currated commands saving which in real life would save weight on the rover on computers and having better
communication from the big antenna in space, but it was just too much.

Very sorry, there is definitively a better solution, but I cant think of any that are quick enough 
to be implemented with the current time. The main problem I have is with global variables 
that need to be accessed by reference which isn't possible by simple import as the file needs to be started.
 Instead we tried to separate the code with this block of text and a bunch of endlines.



tl:dr: couldn't find a way to seperate all the code in folders, so heres a block of text
and end-lines instead. Sorry, we really put some time to thought into it and left residual code as a proof.
"""












class ProgramNode(AbstractNode):

    def check_scope(self, desc, assi):
        self.nodes[0].check_scope([], [])

    def check_semantics(self):
        self.nodes[0].check_semantics()

    def name(self):
        return "Program"

    def parse(self):
        if self.verify_and_add_token(0, BlockNode()):
            return True

        else:
            raise Exception("program rejected parse")


"""class GenericNode(AbstractNode):

    def __init__(self, scope, string):
        super().__init__(scope)
        self.name1 = string
        self.nodes = None

    def name(self):
        return self.name1

    def parse(self):
        return True
        """


class BlockNode(AbstractNode):

    def check_scope(self, decl_list, assign_list):
        decl_list.append([])
        assign_list.append([])
        decl_list, assign_list = super().check_scope(decl_list, assign_list)
        decl_list.pop()
        assign_list.pop()
        return decl_list, assign_list

    def run(self):

        self.scope = CURRENT_SCOPE.copy()

        for key in CURRENT_SCOPE.keys():
            CURRENT_SCOPE[key]["redeclared"] = False

        for child in self.nodes:
            if child is not None:
                child.run()

        self.end_of_block_scope()

    def end_of_block_scope(self):

        # remove all redeclared arguments
        for key in CURRENT_SCOPE:
            if CURRENT_SCOPE[key]["redeclared"]:
                del CURRENT_SCOPE[key]

        # get all non redeclared keys
        keys = CURRENT_SCOPE.keys()

        # for all keys that were removed or are now nonexistent, replace them with original if they exist
        for key in self.scope:
            if key not in keys:
                CURRENT_SCOPE[key] = self.scope[key]

    def name(self):
        return "Block"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "{") \
                and self.verify_and_add_token(1, DeclsNode()) \
                and self.verify_and_add_token(2, StmtsNode()) \
                and self.verify_and_add_non_token_node(3, "}"):
            return True
        else:
            return False


class DeclsNode(AbstractNode):
    def name(self):
        return "Decls"

    def parse(self):
        if self.verify_and_add_token(0, DeclNode()) \
                and self.verify_and_add_token(1, DeclsNode()):

            return True
        else:
            return None

    def check_semantics(self):
        pass


class DeclNode(AbstractNode):

    def name(self):
        return "Decl"

    def run(self):
        ob_type = self.nodes[0].get_type(None)
        self.nodes[1].set_type(ob_type)

    def parse(self):
        if self.verify_and_add_token(0, TypeNode()) \
                and self.verify_and_add_token(1, IDNode()) \
                and self.verify_and_add_non_token_node(2, ";"):
            self.nodes[1].set_type(self.nodes[0].get_type(None))
            return True
        else:
            return False

    def check_scope(self, decl_list, assign_list):
        next(reversed(decl_list)).append(self.nodes[1].get_id())
        return decl_list, assign_list


class TypeNode(AbstractNode):

    def name(self):
        return "Type"

    def get_type(self, ob_type):
        return self.nodes[0].get_type(None)

    def parse(self):
        if self.verify_and_add_token(0, BasicNode()):
            return True
        else:
            return False


class StmtsNode(AbstractNode):

    def name(self):
        return "stmts"

    def parse(self):
        # since python uses lazy eval, this shouldn't create an infinite loop
        if self.verify_and_add_token(0, StmtNode()) \
                and self.verify_and_add_token(1, StmtsNode()):

            return True
        else:
            return None


class StmtNode(AbstractNode):

    def check_scope(self, decl_list, assign_list):

        if self.option == 0 and self.nodes[0].get_id() in decl_list:
            ids = self.nodes[2].get_Ids([])
            if all((item or any(item in sub_assign_list
                                for sub_assign_list in assign_list)) for item in
                   ids):  # item cannot be 1 or 0 as it will be rejected
                next(reversed(assign_list)).append(self.nodes[0].get_id())
                return decl_list, assign_list

        elif self.option == 1 or self.option == 2 or self.option == 3:
            ids = self.nodes[2].get_Ids([])
            if all((item or any(item in sub_assign_list
                                for sub_assign_list in assign_list)) for item in ids):
                return super().check_scope(decl_list, assign_list)

        elif self.option == 4:
            return super().check_scope(decl_list, assign_list)

        raise Exception("var not in scope")

    def check_semantics(self):
        if self.option == 0:
            if not (self.nodes[0].get_type(None) == "int"
                    and self.nodes[2].get_type(self.nodes[0].get_type(None)) == "int") \
                    or (self.nodes[0].get_type(None) == "double"
                        and (self.nodes[2].get_type == "int"
                             or self.nodes[2].get_type(self.nodes[0].get_type(None)) == "double")) \
                    or (self.nodes[0].get_type(None) ==
                        self.nodes[2].get_type(self.nodes[2].get_type(self.nodes[0].get_type(None)))):
                raise Exception("bad typing")

        elif self.option == 1 or self.option == 2 or self.option == 3:
            if self.nodes[2].get_type() != "bool":
                raise Exception("bad typing")

        elif self.option == 4:
            self.nodes[0].check_semantics()

    def run(self):
        if self.option == 0:
            self.nodes[0].set_value(self.nodes[2].get_value())

        elif self.option == 1:
            if self.nodes[2].get_value():
                self.nodes[4].run()
            else:
                self.nodes[6].run()

        elif self.option == 2:
            if self.nodes[2].get_value():
                self.nodes[4].run()

        elif self.option == 3:
            while self.nodes[2].get_value():
                self.nodes[4].run()
        elif self.option == 4:
            self.nodes[0].run()

    def name(self):
        return "Stmt"

    def parse(self):
        if self.verify_and_add_token(0, LocNode()) \
                and self.verify_and_add_non_token_node(1, "=") \
                and self.verify_and_add_token(2, BoolNode()) \
                and self.verify_and_add_non_token_node(3, ";"):
            self.option = 0

            return True
        elif self.reset() \
                and self.verify_and_add_non_token_node(0, "if") \
                and self.verify_and_add_non_token_node(1, "(") \
                and self.verify_and_add_token(2, BoolNode()) \
                and self.verify_and_add_non_token_node(3, ")") \
                and self.verify_and_add_token(4, StmtNode()) \
                and self.verify_and_add_non_token_node(5, "else") \
                and self.verify_and_add_token(6, StmtNode()):
            self.option = 1

            return True

        elif self.reset() \
                and self.verify_and_add_non_token_node(0, "if") \
                and self.verify_and_add_non_token_node(1, "(") \
                and self.verify_and_add_token(2, BoolNode()) \
                and self.verify_and_add_non_token_node(3, ")") \
                and self.verify_and_add_token(4, StmtNode()):
            self.option = 2

            return True


        elif self.reset() \
                and self.verify_and_add_non_token_node(0, "while") \
                and self.verify_and_add_non_token_node(1, "(") \
                and self.verify_and_add_token(2, BoolNode()) \
                and self.verify_and_add_non_token_node(3, ")") \
                and self.verify_and_add_token(4, StmtNode()):
            self.option = 3

            return True

        elif self.reset() \
                and self.verify_and_add_token(0, BlockNode()):
            self.option = 4

            return True

        else:
            return False


class IDNode(AbstractNode):
    value = ""

    def get_Ids(self, id_list):
        return id_list.append(self.get_id())

    def name(self):
        return "ID"

    def get_id(self):
        return str(self.value)

    def get_value(self):
        if self.get_id() in GLOBAL_SCOPE.keys():
            return GLOBAL_SCOPE[self.get_id()]["value"]
        return CURRENT_SCOPE[self.get_id()]["value"]

    def set_value(self, value):
        if self.get_id() in GLOBAL_SCOPE.keys():
            GLOBAL_SCOPE[self.get_id()]["value"] = value
        CURRENT_SCOPE[self.get_id()]["value"] = value

    def get_type(self, ob_type):
        if self.get_id() in GLOBAL_SCOPE.keys():
            return GLOBAL_SCOPE[self.get_id()]["type"]
        return CURRENT_SCOPE[self.get_id()]["type"]

    def set_type(self, ob_type):
        if self.get_id() in GLOBAL_SCOPE.keys():
            raise Exception("cannot reassign namespace var")
        CURRENT_SCOPE[self.get_id()] = {"redeclared": True, "type": str(ob_type)}

    def parse(self):
        reserved_symbole = {"{", "}", "[", "]", ";", "int", "bool", "char", "double", "="}
        token = self.get_token()
        if token not in reserved_symbole and not token.isdigit():
            self.value = self.get_token()
            self.iterate_cursor()
            return True
        else:
            return False


class LocNode(AbstractNode):

    def get_value(self):
        return self.nodes[0].get_value()

    def set_value(self, value, scope):
        return self.nodes[0].set_value(value, scope)

    def get_type(self, ob_type):
        return self.nodes[0].get_type(ob_type)

    def name(self):
        return "Loc"

    def parse(self):
        if self.verify_and_add_token(0, IDNode()):
            return True
        else:
            return False

    def check_scope(self, decl_list, assign_list):
        my_id = self.nodes[0].get_id()
        for arrays in assign_list:
            for item in arrays:
                if my_id == item:
                    return decl_list, assign_list

        for command in GLOBAL_SCOPE.keys():
            if command == id:
                return decl_list, assign_list

        raise Exception("id not found " + self.nodes[0].get_id())


class BoolNode(AbstractNode):

    def get_type(self, ob_type):
        if len(self.nodes) == 2:
            if ob_type == "bool" and (self.check_childs(0, "bool", ob_type) and self.check_childs(1, "bool", ob_type)):
                return "bool"
            else:
                Exception("bool issue")
        else:
            return self.get_child_type(0, ob_type)

    def get_value(self):
        if len(self.nodes) == 2:
            val = self.nodes[1].get_value()
            return self.nodes[0].get_value() or val
        else:
            return self.nodes[0].get_value()

    def name(self):
        return "Bool"

    def parse(self):
        if self.verify_and_add_token(0, JoinNode()) \
                and self.verify_and_add_token(1, BoolClNode()):
            return True

        else:
            return False


class BoolClNode(AbstractNode):

    def get_type(self, ob_type):
        if len(self.nodes) == 3:
            if (ob_type == "bool") and (
                    self.check_childs(0, "bool", ob_type) and self.check_childs(1, "bool", ob_type)):
                return "bool"
            else:
                Exception("boolCl issue")
        elif self.check_childs(1, "bool", ob_type):
            return "bool"
        else:
            Exception("boolCl issue")

    def get_value(self):
        if len(self.nodes) == 3:
            val = self.nodes[2].get_value()
            return self.nodes[1].get_value() or val
        else:
            return self.nodes[1].get_value()

    def name(self):
        return "BoolCl"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "||") \
                and self.verify_and_add_token(1, JoinNode()) \
                and self.verify_and_add_token(2, BoolClNode()):
            return True

        else:
            return None


class JoinNode(AbstractNode):

    def get_type(self, ob_type):
        if len(self.nodes) == 2:
            if ob_type == "bool" and (self.check_childs(0, "bool", ob_type) and self.check_childs(1, "bool", ob_type)):
                return "bool"
            else:
                Exception("join issue")
        else:
            return self.get_child_type(0, ob_type)

    def get_value(self):
        if len(self.nodes) == 2:
            val = self.nodes[1].get_value()
            return self.nodes[0].get_value() and val
        else:
            return self.nodes[0].get_value()

    def name(self):
        return "Join"

    def parse(self):
        if self.verify_and_add_token(0, EqualityNode()) \
                and self.verify_and_add_token(1, JoinClNode()):
            return True
        else:
            return False


class JoinClNode(AbstractNode):

    def get_type(self, ob_type):
        if len(self.nodes) == 3:
            if (ob_type == "bool") and (
                    self.check_childs(1, "bool", ob_type) and self.check_childs(2, "bool", ob_type)):
                return "bool"
            else:
                Exception("boolCl issue")
        elif self.check_childs(1, "bool", ob_type):
            return "bool"
        else:
            Exception("joinCl issue")

    def get_value(self):
        if len(self.nodes) == 3:
            val = self.nodes[2].get_value()
            return self.nodes[1].get_value() and val
        else:
            return self.nodes[1].get_value()

    def name(self):
        return "JoinCl"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "&&") \
                and self.verify_and_add_token(1, EqualityNode()) \
                and self.verify_and_add_token(2, JoinClNode()):
            return True

        else:
            return None


class EqualityNode(AbstractNode):

    def get_type(self, ob_type):
        if len(self.nodes) == 2:
            if (ob_type == "bool") and (
                    ((self.check_childs(0, "int", ob_type) or self.check_childs(0, "double", ob_type))
                     and (self.check_childs(1, "int", ob_type) or self.check_childs(1, "double", ob_type)))
                    or (self.check_childs(0, "bool", ob_type) and self.check_childs(1, "bool", ob_type))):
                return "bool"
            else:
                Exception("rel issue")
        else:
            return self.get_child_type(0, ob_type)

    def get_value(self):
        if len(self.nodes) == 2:
            val, op = self.nodes[1].get_value()
            if op == "==":
                return self.nodes[0].get_value() == val
            elif op == "!=":
                return self.nodes[0].get_value() != val
        else:
            return self.nodes[0].get_value()

    def name(self):
        return "Equality"

    def parse(self):
        if self.verify_and_add_token(0, RelNode()) \
                and self.verify_and_add_token(1, EqualityClNode()):

            return True
        else:
            return False


class EqualityClNode(AbstractNode):

    def get_type(self, ob_type):
        if len(self.nodes) == 3:
            if (ob_type == "bool") and (
                    ((self.check_childs(1, "int", ob_type) or self.check_childs(1, "double", ob_type))
                     and (self.check_childs(2, "int", ob_type) or self.check_childs(2, "double", ob_type)))
                    or (self.check_childs(2, "bool", ob_type) and self.check_childs(1, "bool", ob_type))):
                return "bool"
            else:
                raise Exception("eaqualityCl issue")
        else:
            self.get_child_type(1, ob_type)

    def get_value(self):
        if len(self.nodes) == 3:
            val, op = self.nodes[2].get_value()
            if op == "==":
                return self.nodes[1].get_value() == val, self.option
            elif op == "!=":
                return self.nodes[1].get_value() != val, self.option
        else:
            return self.nodes[1].get_value(), self.option

    def name(self):
        return "EqualityCl"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "==") \
                and self.verify_and_add_token(1, RelNode()) \
                and self.verify_and_add_token(2, EqualityClNode()):
            self.option = "=="
            return True

        elif self.reset() \
                and self.verify_and_add_non_token_node(0, "!=") \
                and self.verify_and_add_token(1, RelNode()) \
                and self.verify_and_add_token(2, EqualityClNode()):
            self.option = "!="
            return True
        else:
            return None


class RelNode(AbstractNode):

    def get_type(self, ob_type):
        if len(self.nodes) == 2:
            if (ob_type == "bool") and (self.check_childs(0, "int", ob_type)
                                        or self.check_childs(0, "double", ob_type)) \
                    and (self.check_childs(1, "int", ob_type) or self.check_childs(1, "double", ob_type)):
                return "bool"
            else:
                Exception("rel issue")
        else:
            return self.get_child_type(0, ob_type)

    def get_value(self):
        if len(self.nodes) == 2:
            val, op = self.nodes[1].get_value()
            if op == "<":
                return self.nodes[0].get_value() < val
            elif op == "<=":
                return self.nodes[0].get_value() <= val
            elif op == ">":
                return self.nodes[0].get_value() > val
            elif op == ">=":
                return self.nodes[0].get_value() >= val
        else:
            return self.nodes[0].get_value()

    def name(self):
        return "Rel"

    def parse(self):
        if self.verify_and_add_token(0, ExprNode()) \
                and self.verify_and_add_token(1, RelTailNode()):

            return True
        else:
            return False


class RelTailNode(AbstractNode):

    def get_type(self, ob_type):
        if (ob_type == "bool") and (self.check_childs(1, "int", ob_type) or self.check_childs(1, "double", ob_type)):
            return self.get_child_type(1, ob_type)
        else:
            Exception("rel tail issue")

    def get_value(self):
        return self.nodes[1].get_value(), self.option

    def name(self):
        return "RelTail"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "<") \
                and self.verify_and_add_token(1, ExprNode()):
            self.option = "<"
            return True
        elif self.reset() \
                and self.verify_and_add_non_token_node(0, ">") \
                and self.verify_and_add_token(1, ExprNode()):
            self.option = ">"
            return True
        elif self.reset() \
                and self.verify_and_add_non_token_node(0, "<=") \
                and self.verify_and_add_token(1, ExprNode()):
            self.option = "<="
            return True
        elif self.reset() \
                and self.verify_and_add_non_token_node(0, ">=") \
                and self.verify_and_add_token(1, ExprNode()):
            self.option = ">="
            return True
        else:
            return None


class ExprNode(AbstractNode):

    def get_type(self, ob_type):
        if len(self.nodes) == 2:
            if not (self.check_childs(0, "int", ob_type) or self.check_childs(0, "double", ob_type)) \
                    and not (self.check_childs(1, "int", ob_type) or self.check_childs(1, "double", ob_type)):
                raise Exception("Term tail does not agree")
        else:
            return self.get_child_type(0, ob_type)

    def get_value(self):
        if len(self.nodes) == 2:
            val, op = self.nodes[1].get_value()
            if op == "+":
                return self.nodes[0].get_value() + val
            else:
                return self.nodes[0].get_value() - val
        else:
            return self.nodes[0].get_value()

    def name(self):
        return "Expr"

    def parse(self):
        if self.verify_and_add_token(0, TermNode()) \
                and self.verify_and_add_token(1, ExprTailNode()):

            return True
        else:
            return False


class ExprTailNode(AbstractNode):

    def get_type(self, ob_type):
        if (ob_type == "int" or ob_type == "double") \
                and (self.check_childs(1, "int", ob_type) or self.check_childs(1, "double", ob_type)):
            if len(self.nodes) == 3:
                if not (self.check_childs(2, "int", ob_type) or self.check_childs(2, "double", ob_type)):
                    raise Exception()
            return self.get_child_type(1, ob_type)
        else:
            raise Exception("expr tail does not agree")

    def get_value(self):
        if len(self.nodes) == 3:
            val, op = self.nodes[2].get_value()
            if op == "+":
                return self.nodes[1].get_value() + val, self.option
            else:
                return self.nodes[1].get_value() - val, self.option
        else:
            return self.nodes[1].get_value(), self.option

    def name(self):
        return "ExprTail"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "+") \
                and self.verify_and_add_token(1, TermNode()) \
                and self.verify_and_add_token(2, ExprTailNode()):
            self.option = "+"
            return True
        elif self.reset() \
                and self.verify_and_add_non_token_node(0, "-") \
                and self.verify_and_add_token(1, TermNode()) \
                and self.verify_and_add_token(2, ExprTailNode()):
            self.option = "-"
            return True
        else:
            return None


class TermNode(AbstractNode):

    def get_type(self, ob_type):
        if len(self.nodes) == 3:
            if not (self.check_childs(0, "int", ob_type) or self.check_childs(0, "double", ob_type)) \
                    or not (self.check_childs(1, "int", ob_type) or self.check_childs(1, "double", ob_type)):
                raise Exception("Term tail does not agree")
            return self.get_child_type(1, ob_type)
        else:
            return self.get_child_type(0, ob_type)

    def get_value(self):
        if len(self.nodes) == 2:
            val, op = self.nodes[1].get_value()
            if op == "*":
                return self.nodes[0].get_value() * val
            else:
                return self.nodes[0].get_value() / val
        else:
            return self.nodes[0].get_value()

    def name(self):
        return "Term"

    def parse(self):
        if self.verify_and_add_token(0, UnaryNode()) \
                and self.verify_and_add_token(1, TermTailNode()):

            return True
        else:
            return False


class TermTailNode(AbstractNode):

    def get_value(self):
        if len(self.nodes) == 3:
            val, op = self.nodes[2].get_value()
            if op == "*":
                return (val * self.nodes[1].get_value()), self.option
            else:
                return (val / self.nodes[1].get_value()), self.option
        return self.nodes[1].get_value(), self.option

    def get_type(self, ob_type):
        if (ob_type != "int" or ob_type != "double") \
                and (self.check_childs(1, "int", ob_type) or self.check_childs(1, "double", ob_type)):
            if len(self.nodes) == 3:
                if not (self.check_childs(2, "int", ob_type) or self.check_childs(2, "double", ob_type)):
                    raise Exception("term tail does not agree")
            return self.get_child_type(1, ob_type)
        else:
            raise Exception("term tail does not agree")

    def name(self):
        return "TermTail"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "*") \
                and self.verify_and_add_token(1, UnaryNode()) \
                and self.verify_and_add_token(2, TermTailNode()):
            self.option = "*"
            return True

        elif self.reset() \
                and self.verify_and_add_non_token_node(0, "/") \
                and self.verify_and_add_token(1, UnaryNode()) \
                and self.verify_and_add_token(2, TermTailNode()):
            self.option = "/"
            return True

        else:
            return None


class UnaryNode(AbstractNode):

    def get_type(self, ob_type):
        if self.option == 0:
            if self.nodes[1].get_type(ob_type) == "bool":
                return "bool"

        elif self.option == 1:
            if self.nodes[1].get_type(ob_type) == "int" or self.nodes[1].get_type(ob_type) == "double":
                return self.nodes[1].get_type(ob_type)

        elif self.option == 2:
            return self.nodes[0].get_type(ob_type)
        raise Exception("bad unary ob_type")

    def get_value(self):
        if self.option == 0:
            my_bool = not self.nodes[1].get_value()
            return my_bool
        elif self.option == 1:
            return self.nodes[1].get_value() * -1
        elif self.option == 2:
            return self.nodes[0].get_value()

    def name(self):
        return "Unary"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "!") \
                and self.verify_and_add_token(1, UnaryNode()):
            self.option = 0
            return True


        elif self.reset() \
                and self.verify_and_add_non_token_node(0, "-") \
                and self.verify_and_add_token(1, UnaryNode()):
            self.option = 1
            return True

        elif self.reset() \
                and self.verify_and_add_token(0, FactorNode()):
            self.option = 2
            return True
        else:
            return False


class FactorNode(AbstractNode):
    reserved_symbole = {"{", "}", "[", "]", ";", "int", "bool", "char", "double", "=", "True", "False"}

    types = []

    ob_type = ""

    val = None

    def get_Ids(self, id_list):
        if self.option == 2:
            id_list.append(True)
            return id_list
        elif self.option == 0:
            return self.nodes[1].get_Ids(id_list)
        else:
            return self.nodes[0].get_Ids(id_list)

    def get_value(self):
        if self.option == 0:
            return self.nodes[1].get_value()
        elif self.option == 1:
            return self.nodes[0].get_value()
        else:
            return self.val

    def get_type(self, ob_type):
        if self.option == 2:
            if ob_type == "bool":
                if "bool" in self.types:
                    self.ob_type = "bool"
                    self.val = bool(self.val)
                    return "bool"
                else:
                    return self.types[0]
            elif ob_type == "int":
                if "int" in self.types:
                    self.val = int(self.val)
                    self.ob_type = "int"
                    return "int"
                else:
                    return self.types[0]
            elif ob_type == "double":
                if "double" in self.types:
                    self.val = float(self.val)
                    self.ob_type = "double"
                    return "double"
                else:
                    return self.types[0]
            else:
                raise Exception("not correct ob_type")
        elif self.option == 0:
            self.ob_type = self.nodes[1].get_type(ob_type)
            return self.ob_type
        else:
            self.ob_type = self.nodes[0].get_type(ob_type)
            return self.ob_type

    def name(self):
        return "Factor"

    def parse(self):
        token = self.get_token()
        if token not in self.reserved_symbole:
            if self.verify_and_add_non_token_node(0, "(") \
                    and self.verify_and_add_token(1, BoolNode()) \
                    and self.verify_and_add_non_token_node(2, ")"):
                self.option = 0
                return True

            elif self.reset() \
                    and not self.is_type() \
                    and self.verify_and_add_token(0, LocNode()):
                self.option = 1
                return True

            elif self.reset() and self.is_type():
                # self.nodes.append(GenericNode(self.get_token()))
                self.val = self.get_token()
                self.option = 2
                self.iterate_cursor()

                return True
            else:
                return False
        else:
            return False

    def is_type(self):
        string = str(self.get_token())
        # checks if string is a double (python floats are double by default)
        if string.replace('.', '', 1).isdigit():
            self.types.append("double")
        if string.isdigit():
            self.types.append("int")
        if string == "True" or string == "False":
            self.types.append("bool")
        if len(self.types) != 0:
            return True
        else:
            return False