# Jerome Sparnaay, Muhi Eddin Tahhan
import sys



"""
Create nodes + parse tree using grammar:

   <program>  ::= <block>
   <block>    ::= { <decls> <stmts> }
   <decls>    ::= e 
                | <decl> <decls>
   <decl>     ::= <type> ID ;
   <type>     ::= BASIC <typecl>
   <typecl>   ::= e 
                | [ NUM ] <typecl>
   <stmts>    ::= e 
                | <stmt> <stmts>
   <stmt>     ::= <loc> = <bool> ;
                | IF ( <bool> ) <stmt>
                | IF ( <bool> ) <stmt> ELSE <stmt>
                | WHILE ( <bool> ) <stmt>
                | <block>
                | ROVER <command>;
   <command>  ::= TOKENCOMMAND <operandl>
   <operandl> ::= e
                | <operand> <operandl>
   <operand>  ::= <bool>
   <loc>      ::= ID <loccl>
   <loccl>    ::= e 
                | [ <bool> ] <loccl>
   <bool>     ::= <join> <boolcl>
   <boolcl>   ::= e 
                | || <join> <boolcl>
   <join>     ::= <equality> <joincl>
   <joincl>   ::= e 
                | && <equality> <joincl>
   <equality> ::= <rel> <equalcl>
   <equalcl>  ::= e 
                | == <rel> <equalcl> 
                | != <rel> <equalcl>
   <rel>      ::= <expr> <reltail>
   <reltail>  ::= e 
                | <= <expr>
                | >= <expr>
                | > <expr>
                | < <expr>
   <expr>     ::= <term> <exprcl>
   <exprcl>   ::= e
                | + <term> <exprcl>
                | - <term> <exprcl>
   <term>     ::= <unary> <termcl>
   <termcl>   ::= e
                | * <unary> <termcl>
                | / <unary> <termcl>
   <unary>    ::= ! <unary>
                | - <unary>
                | <factor>
   <factor>   ::= ( <bool> )
                | <loc>
                | NUM
                | REAL
                | TRUE
                | FALSE


"""

#   The parser works by chaining inside if statements verifications and tree building. We translate
#   the rules by creating a node and passing it to a common verifier (this is the one from the super class)
#   . Then the node is parsed inside the verifier and the return value is used to determine if the node is attached
#   or not to the parent tree. this happens for each node recursively and when the parser arrives at a non-token node,
#   it verifies if the name is legal and parses moves the cursor to the next token of code. this effectively makes
#   this whole parser just a big if statement linked together and the final value of this of programNode
#   is if the string is pared or not. An exception error can be created, but the output is still a bit buggy.
#   Also note, that the string to be parsed has a first pass to tokenize the string between each space,
#   then a program root node is created and parsed. The whole parser uses global variable for the cursor and parse
#   string for simplicity’s sake. All nodes are created from the same AbstractNode, so they have very similar functions.

cursor = 0

def go_right():
    pass


def go_up():
    pass


def go_left():
    pass


def go_down():
    pass


def can_go_down():
    pass


def can_go_left():
    pass


def can_go_up():
    pass


def can_go_right():
    pass


def get_ground():
    pass


def dig():
    pass


def set_ground():
    pass


GLOBAL_SCOPE = {
    "null": {"value": 0}
    , "operand": {"value": 0}
    , "goRight": {"value": go_right()}
    , "goUp": {"value": go_up()}
    , "goLeft": {"value": go_left()}
    , "goDown": {"value": go_down()}
    , "canGoRight": {"value": can_go_right()}
    , "canGoUp": {"value": can_go_up()}
    , "canGoLeft": {"value": can_go_left()}
    , "canGoDown": {"value": can_go_down()}
    , "getGround": {"value": get_ground()}
    , "setGround": {"value": set_ground()}
    , "dig": {"value": dig()}
    , "turnRight": {"value"}
}


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


    def run(self):
        raise Exception("run not instantiated")

    def get_type(self):
        return None

    def set_value(self):
        pass

    def get_value(self):
        return None

    def make_scope(self):
        for child in self.nodes:
            child.make_scope()

    def check_scope(self):
        for child in self.nodes:
            child.check_scope()

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


    def check_scope(self):
        for child in self.nodes:
            child.check_scope()

    def parse(self):
        return True

    def check_semantics(self):
        for child in self.nodes:
            child.check_semantics()



class BasicNode(AbstractNode):

    basic = {"int", "bool", "char", "double"}

    type = ""

    def name(self):
        return type

    def parse(self):
        token = code[cursor]
        if token in self.basic:
            # self.nodes.append(GenericNode(token))
            self.iterate_cursor()
            self.type = token
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

                return True
        else:
            return False


class TypeNode(AbstractNode):

    def name(self):
        return "Type"

    def parse(self):
        if self.verify_and_add_token(0, BasicNode(self.scope))\
            and self.verify_and_add_token(1, TypeClNode(self.scope)):

                    return True
        else:
            return False

class TypeClNode(AbstractNode):

    def name(self):
        return "TypeCl"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "[")\
            and self.verify_and_add_token(1, NumNode(self.scope))\
            and self.verify_and_add_non_token_node(2, "]"):

                    return True
        else:
            return None


class NumNode(AbstractNode):

    value = 0
    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value
    def name(self):
        return "NumNode"

    def parse(self):
        if code[cursor].isdigit():
            self.set_value(code[cursor])
            self.iterate_cursor()
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


class IDNode(AbstractNode):

    def name(self):
        "ID"

    def parse(self):
        reserved_symbole = {"{", "}", "[", "]", ";", "int", "bool", "char", "double", "="}
        token = code[cursor]
        if token not in reserved_symbole and not token.isdigit():
            self.nodes.append(GenericNode(code[cursor]))
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
            and self.verify_and_add_non_token_node(1, "||")\
            and self.verify_and_add_token(2, BoolNode(self.scope)):

                    return True
        elif self.reset()\
                and self.verify_and_add_token(0, JoinNode(self.scope)):
                        return True
        else:
            return False

class JoinNode(AbstractNode):

    def name(self):
        return "Join"

    def parse(self):
        if self.verify_and_add_token(0, EqualityNode(self.scope))\
            and self.verify_and_add_non_token_node(1, "&&")\
            and self.verify_and_add_token(2, BoolNode(self.scope)):

                    return True
        elif self.reset()\
            and self.verify_and_add_token(0, EqualityNode(self.scope)):

                    return True
        else:
            return False

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

                    return True

        elif self.reset()\
                and self.verify_and_add_non_token_node(0, "!=")\
                and self.verify_and_add_token(1, EqualityClNode(self.scope)):

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

                    return True
        elif self.reset()\
            and self.verify_and_add_non_token_node(0, ">")\
            and self.verify_and_add_token(1, ExprNode(self.scope)):

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

                    return True
        elif self.reset()\
                and self.verify_and_add_non_token_node(0, "-")\
                and self.verify_and_add_token(1, ExprTailNode(self.scope)):

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
                    self.nodes.append(GenericNode(code[cursor]))
                    self.iterate_cursor()

                    return True
            else:
                return False
        else:
            return False


node = ProgramNode()
node.parse()

printNode(node, [])