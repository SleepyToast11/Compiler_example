# Jerome Sparnaay, Muhi Eddin Tahhan
import sys
from old_code_component import (
GLOBAL_SCOPE
)



cursor = 0


def convert(code):
    array = code.split()
    return array

def parseExeption(string):
    print("parse error at: " + str(cursor) + " where is " + code[cursor] + " expecting " + string)




inp = open(str(sys.argv[1]))


code = convert(inp)



class AbstractNode():

    option = None
    def __init__(self, scope):
        self.initial_cursor = cursor
        self.nodes = []
        self.scope = scope

    def end_of_token_scope(self, scope):
        for key in self.old_scope:
            if self.scope[key]["value"] != scope[key]["value"]:
                self.scope[key] = scope[key]


    def run(self):
        return None
        """
        this is the general idea of how this should work for most
        for child in self.nodes:
            new_scope = child.run()
            self.end_of_token_scope(new_scope)
            """


    def get_type(self):
        return None

    def set_value(self):
        pass

    def get_value(self):
        return None

    def check_semantics(self):
        for child in self.nodes:
            child.check_semantics()

    def __init__(self, scope):
        self.initial_cursor = cursor
        self.nodes = []
        self.scope = scope


    def name(self):
        return None

    def reset(self):
        global cursor
        cursor = self.initial_cursor
        return True

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

    def verify_and_add_non_token_node(self, string):
        if code[cursor] is string:
            #self.nodes.append(GenericNode(string)) removed simplify runtime interpretation
            self.iterate_cursor()
            return True
        else:
            return False


    def check_scope(self, list):
        for child in self.nodes:
            list = child.check_scope(list)
        return list

    def parse(self):
        return True

    def check_semantics(self):
        for child in self.nodes:
            child.check_semantics()



class BasicNode(AbstractNode):

    basic = {"int", "bool", "char", "double"}



    def name(self):
        return "BasicNode"

    def get_type(self):
        return self.option

    def parse(self):
        token = code[cursor]
        if token in self.basic:
            # self.nodes.append(GenericNode(token))
            self.iterate_cursor()
            self.option = token
            return True
        else:
            return False


class ProgramNode(AbstractNode):

    def name(self):
        return "Program"

    def parse(self):
        if self.verify_and_add_token(0, BlockNode({})):
            return True

        else:
            parseExeption("?")

    def check_scope(self):
        #there is only a block, so it doesn't matter
        for child in self.nodes:
            child.check_scope([])


class GenericNode(AbstractNode):

    def __init__(self, scope, string):
        super().__init__(scope)
        self.name1 = string
        self.nodes = None

    def name(self):
        return self.name1

    def parse(self):
        return True


class BlockNode(AbstractNode):

    def __init__(self, scope):
        self.super(scope)
        self.old_scope = scope
        self.scope = {}
        for key in scope:
            self.scope[key] = scope[key]
            self.scope[key]["redeclared"] = False

    def end_of_block_scope(self):
        for key in self.old_scope:
            if not self.scope[key]["redeclared"]:
                self.old_scope[key]["value"] = self.scope[key]["value"]

    def name(self):
        return "Block"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "{")\
            and self.verify_and_add_token(1, DeclsNode(self.scope))\
            and self.verify_and_add_token(2, StmtsNode(self.scope))\
            and self.verify_and_add_non_token_node(3, "}"):
                return True
        else:
            return False

    def check_scope(self, list):
        list.appernd([])
        super().check_scope(list)
        list.pop()
        return list

class DeclsNode(AbstractNode):
    def name(self):
        return "Decls"

    def parse(self):
        if self.verify_and_add_token(0, DeclNode(self.scope))\
            and self.verify_and_add_token(1, DeclsNode(self.scope)):

                return True
        else:
            return None

class DeclNode(AbstractNode):

    def name(self):
        return "Decl"

    def parse(self):
        if self.verify_and_add_token(0, TypeNode(self.scope))\
            and self.verify_and_add_token(1, IDNode(self.scope))\
            and self.verify_and_add_non_token_node(2, ";"):
                self.nodes[1].set_type(self.nodes[0].get_type())
                return True
        else:
            return False

    def check_scope(self, list):
        next(reversed(list)).append(self.nodes[1].get_id())
        return list

class TypeNode(AbstractNode):

    def name(self):
        return "Type"

    def get_type(self):
        return self.nodes[0].get_type()

    def parse(self):
        if self.verify_and_add_token(0, BasicNode(self.scope)):
            return True
        else:
            return False

class StmtsNode(AbstractNode):

    def name(self):
        return "stmts"

    def parse(self):
        #since python uses lazy eval, this shouldnt create an infinite loop
        if self.verify_and_add_token(0, StmtNode(self.scope))\
            and self.verify_and_add_token(1, StmtsNode(self.scope)):

            return True
        else:
            return None


class StmtNode(AbstractNode):

    def name(self):
        return "Stmt"

    def parse(self):
        if self.verify_and_add_token(0, LocNode(self.scope))\
            and self.verify_and_add_non_token_node(1, "=")\
            and self.verify_and_add_token(2, BoolNode(self.scope))\
            and self.verify_and_add_non_token_node(3, ";"):
                    self.option = 0

                    return True

        elif self.reset()\
            and self.verify_and_add_non_token_node(0, "if")\
            and self.verify_and_add_non_token_node(1, "(")\
            and self.verify_and_add_token(2, BoolNode(self.scope))\
            and self.verify_and_add_non_token_node(3, ")")\
            and self.verify_and_add_token(4, StmtNode(self.scope))\
            and self.verify_and_add_non_token_node(5, "else")\
            and self.verify_and_add_token(6, StmtNode(self.scope)):
                    self.option = 1

                    return True

        elif self.reset()\
            and self.verify_and_add_non_token_node(0, "while")\
            and self.verify_and_add_non_token_node(1, "(")\
            and self.verify_and_add_token(2, BoolNode(self.scope))\
            and self.verify_and_add_non_token_node(3, ")")\
            and self.verify_and_add_token(3, StmtNode(self.scope)):
                    self.option = 2

                    return True

        elif self.reset()\
            and self.verify_and_add_token(0, BlockNode(self.scope)):
            self.option = 3

            return True

        else:
            return False

    def check_semantics(self):
        for child in self.nodes:
            child.check_semantics()
        if self.option == 0:
            if self.nodes[0].get_type() != self.nodes[2].get_type:
                raise Exception("bad typing")

        elif self.option == 1 or self.option == 2:
            if self.nodes[2].get_type() != "bool":
                raise Exception("bad typing")


class IDNode(AbstractNode):

    value = ""

    def name(self):
        "ID"

    def get_id(self):
        return str(self.value)

    def get_value(self):
        return self.scope[self.get_id()]["value"]

    def set_value(self, value):
        self.scope[self.get_id()]["value"] = value
        return self.scope

    def get_type(self):
        return self.scope[self.get_id()]["type"]

    def set_type(self, type):
        self.scope[self.get_id()] = {"redeclared": True, "type": str(type)}
        return self.scope

    def parse(self):
        reserved_symbole = {"{", "}", "[", "]", ";", "int", "bool", "char", "double", "="}
        token = code[cursor]
        if token not in reserved_symbole and not token.isdigit():
            self.value = code[cursor]
            self.iterate_cursor()
            return True
        else:
            return False


class LocNode(AbstractNode):

    def name(self):
        return "Loc"

    def parse(self):
        if self.verify_and_add_token(0, IDNode(self.scope))\
            and self.verify_and_add_token(1, LocClNode(self.scope)):

                    return True
        else:
            return False

    def check_scope(self, list):
        id = self.nodes[0].get_id()
        for arrays in list:
            for item in arrays:
                if id == item:
                    return list

        for command in GLOBAL_SCOPE:
            if command == id:
                return list

        raise Exception("id not found" + self.nodes[0].get_id())

class LocClNode(AbstractNode):

    def name(self):
        return "LocCl"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "[")\
            and self.verify_and_add_token(1, BoolNode(self.scope))\
            and self.verify_and_add_non_token_node(2, "]")\
            and self.verify_and_add_token(3, LocClNode(self.scope)):

                    return True
        else:
            return None

class BoolNode(AbstractNode):

    def name(self):
        return "Bool"

    def parse(self):
        if self.verify_and_add_token(0, JoinNode(self.scope))\
            and self.verify_and_add_token(2, BoolClNode(self.scope)):
                return True

        else:
            return False


class BoolClNode(AbstractNode):

    def name(self):
        return "BoolCl"

    def parse(self):
        if  self.verify_and_add_non_token_node(0, "||") \
            and self.verify_and_add_token(1, JoinNode(self.scope)) \
            and self.verify_and_add_token(2, BoolClNode(self.scope)):
                return True

        else:
            return None

class JoinNode(AbstractNode):

    def name(self):
        return "Join"

    def parse(self):
        if self.verify_and_add_token(0, EqualityNode(self.scope))\
            and self.verify_and_add_token(1, JoinClNode(self.scope)):
                    return True
        else:
            return False

class JoinClNode(AbstractNode):

    def name(self):
        return "JoinCl"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "&&")\
            and self.verify_and_add_token(1, EqualityNode(self.scope))\
            and self.verify_and_add_token(2, JoinClNode(self.scope)):
                return True

        else:
            return None



class EqualityNode(AbstractNode):

    def name(self):
        return "Equality"

    def parse(self):
        if self.verify_and_add_token(0, RelNode(self.scope))\
            and self.verify_and_add_token(1, EqualityClNode(self.scope)):

                    return True
        else:
            return False

class EqualityClNode(AbstractNode):

    def name(self):
        return "EqualityCl"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "==")\
            and self.verify_and_add_token(1, EqualityClNode(self.scope)):
                    self.option = "=="
                    return True

        elif self.reset()\
                and self.verify_and_add_non_token_node(0, "!=")\
                and self.verify_and_add_token(1, EqualityClNode(self.scope)):
                        self.option = "!="
                        return True
        else:
            return None

class RelNode(AbstractNode):

    def name(self):
        return "Rel"

    def parse(self):
        if self.verify_and_add_token(0, ExprNode(self.scope))\
            and self.verify_and_add_token(1, RelTailNode(self.scope)):

                return True
        else:
            return False

class RelTailNode(AbstractNode):

    def name(self):
        return "RelTail"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "<")\
            and self.verify_and_add_token(1, ExprNode(self.scope)):
                    self.option = "<"
                    return True
        elif self.reset()\
            and self.verify_and_add_non_token_node(0, ">")\
            and self.verify_and_add_token(1, ExprNode(self.scope)):
                    self.option = ">"
                    return True
        elif self.reset()\
            and self.verify_and_add_non_token_node(0, "<=")\
            and self.verify_and_add_token(1, ExprNode(self.scope)):
                    self.option = "<="
                    return True
        elif self.reset()\
            and self.verify_and_add_non_token_node(0, ">=")\
            and self.verify_and_add_token(1, ExprNode(self.scope)):
                    self.option = ">="
                    return True
        else:
            return None

class ExprNode(AbstractNode):

    def name(self):
        return "Expr"

    def parse(self):
        if self.verify_and_add_token(0, TermNode(self.scope))\
            and self.verify_and_add_token(1, ExprTailNode(self.scope)):

                    return True
        else:
            return False

class ExprTailNode(AbstractNode):



    def name(self):
        return "ExprTail"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "+")\
            and self.verify_and_add_token(1, ExprTailNode(self.scope)):
                    self.operator = "+"
                    return True
        elif self.reset()\
                and self.verify_and_add_non_token_node(0, "-")\
                and self.verify_and_add_token(1, ExprTailNode(self.scope)):
                        self.operator = "-"
                        return True
        else:
            return None

class TermNode(AbstractNode):

    def name(self):
        return "Term"

    def parse(self):
        if self.verify_and_add_token(0, UnaryNode(self.scope))\
            and self.verify_and_add_token(1, TermTailNode(self.scope)):

                    return True
        else:
            return False

class TermTailNode(AbstractNode):



    def name(self):
        return "TermTail"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "*")\
            and self.verify_and_add_token(1, TermNode(self.scope)):

                    return True

        elif self.reset()\
                and self.verify_and_add_non_token_node(0, "/") \
                and self.verify_and_add_token(1, TermNode(self.scope)):

                        return True
        else:
            return None

class UnaryNode(AbstractNode):

    def name(self):
        return "Unary"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "!")\
            and self.verify_and_add_token(1, UnaryNode(self.scope)):

                    return True


        elif self.reset()\
                and self.verify_and_add_non_token_node(0, "-") \
                and self.verify_and_add_token(1, UnaryNode(self.scope)):

                    return True

        elif self.reset()\
            and self.verify_and_add_token(0, FactorNode(self.scope)):

                    return True
        else:
            return False


class FactorNode(AbstractNode):

    reserved_symbole = {"{", "}", "[", "]", ";", "int", "bool", "char", "double", "="}

    value = {}

    types = []


    def name(self):
        return "Factor"

    def parse(self):
        token = code[cursor]
        if token not in self.reserved_symbole:
            if self.verify_and_add_non_token_node(0, "(")\
                and self.verify_and_add_token(1, BoolNode(self.scope))\
                and self.verify_and_add_non_token_node(2, ")"):

                        return True

            elif self.reset()\
                and self.verify_and_add_token(0, LocNode(self.scope)):

                    return True

            elif self.reset():
                    #self.nodes.append(GenericNode(code[cursor]))

                    self.iterate_cursor()

                    return True
            else:
                return False
        else:
            return False

    def is_type(self, value):
        string = str(code[cursor])
        # checks if string is a double (python floats are double by default)
        if string.replace('.', '', 1).isdigit():
            self.types.append("double")
        if string.isdigit():
            self.types.append("int")
        if string == "true" or string == "false":
            self.types.append("bool")


node = ProgramNode()
node.parse()