import pathlib
import time
import traceback

from oldCode import *

# The maximum amount of time that the rover can run in seconds
MAX_RUNTIME = 36000

# Rovers that exist

CURRENT_SCOPE = {}
cursor = 0

# Command file is stored within the rover directory. Here we're building one file
# for each of the rovers defined above


# Constant used to store the rover command for parsing
ROVER_COMMAND_PARSE = {
    "satellite": "",
    "code": []
}


def get_command():
    """Checks, and gets a command from a rovers command file.

    It returns True when something was found, and False
    when nothing was found. It also truncates the contents
    of the file if it found something so that it doesn't
    run the same command again (unless it was re-run from
    the controller/main program).
    """
    fcontent = None
    with pathlib.Path(pathlib.Path(__file__).parent.resolve(), "satellite.txt").open() as f:
        fcontent = f.read()
    if fcontent is not None and fcontent:
        ROVER_COMMAND_PARSE["satellite"] = fcontent
        with pathlib.Path(pathlib.Path(__file__).parent.resolve(), "satellite.txt").open("w+") as f:
            pass
        return True
    return False


class Satelite():

    def print(self, msg):
        print("Satellite: " + msg)

    def parse_and_execute_cmd(self, command):
        self.print(f"Running command: {command}")
        program = ProgramNode()
        program.check_scope(None, None)

    def wait_for_command(self):
        start = time.time()
        while (time.time() - start) < MAX_RUNTIME:
            # Sleep 1 second before trying to check for
            # content again
            self.print("Waiting for command...")
            time.sleep(1)
            if get_command():
                self.print("Found a command...")
                try:
                    self.parse_and_execute_cmd(ROVER_COMMAND_PARSE["satellite"])
                except Exception as e:
                    self.print("Failed to run command")
                    self.print(traceback.format_exc())
                finally:
                    self.print("Finished running command.\n\n")


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
        return ROVER_COMMAND_PARSE["code"][cursor]

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


def main():
    # Initialize the rovers
    satellite = Satelite()

    satellite.wait_for_command()


if __name__ == "__main__":
    main()



