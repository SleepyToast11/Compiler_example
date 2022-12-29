
from oldCode import *

cursor = 0
CURRENT_SCOPE = {}


def convert(code):
    array = code.split()
    return array

def parseExeption(string):
    print(" where is " + AbstractNode.get_token() + " expecting " + string)




inp = open(str(sys.argv[1]))


code = convert(inp)

class Parser():

    def __init__(self, rover):
        self.rover = rover
        program_node = ProgramNode()



class AbstractNode():

    scope = {}
    option = None
    def __init__(self):
        self.initial_cursor = cursor
        self.nodes = []

    def check_childs(self, index, type, superType):
        return self.nodes[index].get_types(superType) == type

    def get_type(self, type):
        pass

    def get_child_type(self, index, type):
        return self.nodes[index].get_type(type)

# generic run function for all nodes, most will not run and be called by other methods like get val or set value
    def run(self):
        for child in self.nodes:
            child.run()

    def check_semantics(self):
        for child in self.nodes:
            child.check_semantics()

    def get_Ids(self, list):
        for child in self.nodes:
            list = child.get_Ids(list)
        return list

    def name(self):
        return None

    def reset(self):
        global cursor
        cursor = self.initial_cursor
        return True

    def get_token(self):
        return code[cursor]

    def verify_and_add_token(self, index, node):
        val = node.parse()
        if val is None:
            return True
        elif val:
            self.nodes.append(node)
            return True
        else:
            return False

    def iterate_cursor(self):
        global cursor
        cursor += 1
        return True

    def verify_and_add_non_token_node(self, index, string):
        if self.get_token() is string:
            #self.nodes.append(GenericNode(string)) removed simplify runtime interpretation
            self.iterate_cursor()
            return True
        else:
            return False


    def check_scope(self, decl_list, assign_list):
        for child in self.nodes:
            decl_list, assign_list = child.check_scope(decl_list, assign_list)
        return decl_list, assign_list

    def parse(self):
        return True
