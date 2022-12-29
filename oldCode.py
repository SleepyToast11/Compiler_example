# Jerome Sparnaay, Muhi Eddin Tahhan
from Abstract_Node_OldCode import AbstractNode
from old_code_component import (
    GLOBAL_SCOPE
)


class BasicNode(AbstractNode):

    basic = {"int", "bool", "double"}



    def name(self):
        return "BasicNode"

    def get_type(self):
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


class ProgramNode(AbstractNode):

    def check_scope(self, decl_list, assign_list):
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

        global CURRENT_SCOPE
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
        if self.verify_and_add_non_token_node(0, "{")\
            and self.verify_and_add_token(1, DeclsNode())\
            and self.verify_and_add_token(2, StmtsNode())\
            and self.verify_and_add_non_token_node(3, "}"):
                return True
        else:
            return False

class DeclsNode(AbstractNode):
    def name(self):
        return "Decls"

    def parse(self):
        if self.verify_and_add_token(0, DeclNode())\
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
        type = self.nodes[0].get_type()
        self.nodes[1].set_type(type)

    def parse(self):
        if self.verify_and_add_token(0, TypeNode())\
            and self.verify_and_add_token(1, IDNode())\
            and self.verify_and_add_non_token_node(2, ";"):
                self.nodes[1].set_type(self.nodes[0].get_type())
                return True
        else:
            return False

    def check_scope(self, decl_list, assign_list):
        next(reversed(decl_list)).append(self.nodes[1].get_id())
        return decl_list, assign_list


class TypeNode(AbstractNode):

    def name(self):
        return "Type"

    def get_type(self):
        return self.nodes[0].get_type()

    def parse(self):
        if self.verify_and_add_token(0, BasicNode()):
            return True
        else:
            return False

class StmtsNode(AbstractNode):

    def name(self):
        return "stmts"

    def parse(self):
        #since python uses lazy eval, this shouldnt create an infinite loop
        if self.verify_and_add_token(0, StmtNode())\
            and self.verify_and_add_token(1, StmtsNode()):

            return True
        else:
            return None


class StmtNode(AbstractNode):

    def check_scope(self, decl_list, assign_list):

        if self.option == 0 and self.nodes[0].get_id() in decl_list:
            ids = self.nodes[2].get_Ids([])
            if all((item or any(item in sub_assign_list
                                for sub_assign_list in assign_list)) for item in ids):     # item cannot be 1 or 0 as it will be rejected
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
            if not (self.nodes[0].get_type() == "int" and self.nodes[2].get_type == "int")\
                    or (self.nodes[0].get_type() == "double"
                        and (self.nodes[2].get_type == "int" or self.nodes[2].get_type == "double"))\
                    or (self.nodes[0].get_type() == self.nodes[2].get_type):
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
        if self.verify_and_add_token(0, LocNode())\
            and self.verify_and_add_non_token_node(1, "=")\
            and self.verify_and_add_token(2, BoolNode())\
            and self.verify_and_add_non_token_node(3, ";"):
                    self.option = 0

                    return True
        elif self.reset()\
            and self.verify_and_add_non_token_node(0, "if")\
            and self.verify_and_add_non_token_node(1, "(")\
            and self.verify_and_add_token(2, BoolNode())\
            and self.verify_and_add_non_token_node(3, ")")\
            and self.verify_and_add_token(4, StmtNode())\
            and self.verify_and_add_non_token_node(5, "else")\
            and self.verify_and_add_token(6, StmtNode()):
                    self.option = 1

                    return True

        elif self.reset()\
            and self.verify_and_add_non_token_node(0, "if")\
            and self.verify_and_add_non_token_node(1, "(")\
            and self.verify_and_add_token(2, BoolNode())\
            and self.verify_and_add_non_token_node(3, ")")\
            and self.verify_and_add_token(4, StmtNode()):
                    self.option = 2

                    return True


        elif self.reset()\
            and self.verify_and_add_non_token_node(0, "while")\
            and self.verify_and_add_non_token_node(1, "(")\
            and self.verify_and_add_token(2, BoolNode())\
            and self.verify_and_add_non_token_node(3, ")")\
            and self.verify_and_add_token(4, StmtNode()):
                    self.option = 3

                    return True

        elif self.reset()\
            and self.verify_and_add_token(0, BlockNode()):
            self.option = 4

            return True

        else:
            return False


class IDNode(AbstractNode):

    value = ""

    def get_Ids(self, list):
        return list.append(self.get_id())
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

    def get_type(self, type):
        if self.get_id() in GLOBAL_SCOPE.keys():
            return GLOBAL_SCOPE[self.get_id()]["type"]
        return CURRENT_SCOPE[self.get_id()]["type"]

    def set_type(self, type):
        if self.get_id() in GLOBAL_SCOPE.keys():
            raise Exception("cannot reassign namespace var")
        CURRENT_SCOPE[self.get_id()] = {"redeclared": True, "type": str(type)}


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

    def get_type(self, type):
        return self.nodes[0].get_type(type)

    def name(self):
        return "Loc"

    def parse(self):
        if self.verify_and_add_token(0, IDNode()):
            return True
        else:
            return False

    def check_scope(self, decl_list, assign_list):
        id = self.nodes[0].get_id()
        for arrays in assign_list:
            for item in arrays:
                if id == item:
                    return decl_list, assign_list

        for command in GLOBAL_SCOPE.keys():
            if command == id:
                return list

        raise Exception("id not found " + self.nodes[0].get_id())

class BoolNode(AbstractNode):

    def get_type(self, type):
        if len(self.nodes) == 2:
            if type == "bool" and (self.check_childs(0, "bool", type) and self.check_childs(1, "bool", type)):
                return "bool"
            else:
                Exception("bool issue")
        else:
            return self.get_child_type(0, type)

    def get_value(self):
        if len(self.nodes) == 2:
            val = self.nodes[1].get_value()
            return self.nodes[0].get_value() or val
        else:
            return self.nodes[0].get_value()


    def name(self):
        return "Bool"

    def parse(self):
        if self.verify_and_add_token(0, JoinNode())\
            and self.verify_and_add_token(1, BoolClNode()):
                return True

        else:
            return False


class BoolClNode(AbstractNode):

    def get_type(self, type):
        if len(self.nodes) == 3:
            if (type == "bool") and (self.check_childs(0, "bool", type) and self.check_childs(1, "bool", type)):
                return "bool"
            else:
                Exception("boolCl issue")
        elif self.check_childs(1, "bool", type):
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
        if  self.verify_and_add_non_token_node(0, "||") \
            and self.verify_and_add_token(1, JoinNode()) \
            and self.verify_and_add_token(2, BoolClNode()):
                return True

        else:
            return None

class JoinNode(AbstractNode):

    def get_type(self, type):
        if len(self.nodes) == 2:
            if type == "bool" and (self.check_childs(0, "bool", type) and self.check_childs(1, "bool", type)):
                return "bool"
            else:
                Exception("join issue")
        else:
            return self.get_child_type(0, type)

    def get_value(self):
        if len(self.nodes) == 2:
            val = self.nodes[1].get_value()
            return self.nodes[0].get_value() and val
        else:
            return self.nodes[0].get_value()

    def name(self):
        return "Join"

    def parse(self):
        if self.verify_and_add_token(0, EqualityNode())\
            and self.verify_and_add_token(1, JoinClNode()):
                    return True
        else:
            return False

class JoinClNode(AbstractNode):

    def get_type(self, type):
        if len(self.nodes) == 3:
            if (type == "bool") and (self.check_childs(1, "bool", type) and self.check_childs(2, "bool", type)):
                return "bool"
            else:
                Exception("boolCl issue")
        elif self.check_childs(1, "bool", type):
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
        if self.verify_and_add_non_token_node(0, "&&")\
            and self.verify_and_add_token(1, EqualityNode())\
            and self.verify_and_add_token(2, JoinClNode()):
                return True

        else:
            return None



class EqualityNode(AbstractNode):

    def get_type(self, type):
        if len(self.nodes) == 2:
            if (type == "bool") and (((self.check_childs(0, "int", type) or self.check_childs(0, "double", type)) \
                and (self.check_childs(1, "int", type) or self.check_childs(1, "double", type)))\
                    or (self.check_childs(0, "bool", type) and self.check_childs(1, "bool", type))):
                    return "bool"
            else:
                Exception("rel issue")
        else:
            return self.get_child_type(0, type)

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
        if self.verify_and_add_token(0, RelNode())\
            and self.verify_and_add_token(1, EqualityClNode()):

                    return True
        else:
            return False

class EqualityClNode(AbstractNode):

    def get_type(self, type):
        if len(self.nodes) == 3:
            if (type == "bool") and (((self.check_childs(1, "int", type) or self.check_childs(1, "double", type)) \
                    and (self.check_childs(2, "int", type) or self.check_childs(2, "double", type)))\
                        or (self.check_childs(2, "bool", type) and self.check_childs(1, "bool", type))):
                    return "bool"
            else:
                raise Exception("eaqualityCl issue")
        else:
            self.get_child_type(1, type)

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
        if self.verify_and_add_non_token_node(0, "==")\
            and self.verify_and_add_token(1, RelNode())\
            and self.verify_and_add_token(2, EqualityClNode()):
                    self.option = "=="
                    return True

        elif self.reset()\
                and self.verify_and_add_non_token_node(0, "!=") \
                and self.verify_and_add_token(1, RelNode()) \
                and self.verify_and_add_token(2, EqualityClNode()):
                        self.option = "!="
                        return True
        else:
            return None

class RelNode(AbstractNode):

    def get_type(self, type):
        if len(self.nodes) == 2:
            if (type == "bool") and (self.check_childs(0, "int", type) or self.check_childs(0, "double", type)) \
                and (self.check_childs(1, "int", type) or self.check_childs(1, "double", type)):
                    return "bool"
            else:
                Exception("rel issue")
        else:
            return self.get_child_type(0, type)

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
        if self.verify_and_add_token(0, ExprNode())\
            and self.verify_and_add_token(1, RelTailNode()):

                return True
        else:
            return False

class RelTailNode(AbstractNode):

    def get_type(self, type):
        if (type == "bool") and (self.check_childs(1, "int", type) or self.check_childs(1, "double", type)):
            return self.get_child_type(1, type)
        else:
            Exception("rel tail issue")

    def get_value(self):
        return self.nodes[1].get_value(), self.option




    def name(self):
        return "RelTail"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "<")\
            and self.verify_and_add_token(1, ExprNode()):
                    self.option = "<"
                    return True
        elif self.reset()\
            and self.verify_and_add_non_token_node(0, ">")\
            and self.verify_and_add_token(1, ExprNode()):
                    self.option = ">"
                    return True
        elif self.reset()\
            and self.verify_and_add_non_token_node(0, "<=")\
            and self.verify_and_add_token(1, ExprNode()):
                    self.option = "<="
                    return True
        elif self.reset()\
            and self.verify_and_add_non_token_node(0, ">=")\
            and self.verify_and_add_token(1, ExprNode()):
                    self.option = ">="
                    return True
        else:
            return None

class ExprNode(AbstractNode):

    def get_type(self, type):
        if len(self.nodes) == 2:
            if not (self.check_childs(0, "int", type) or self.check_childs(0, "double", type))\
                and not ((self.check_childs(1, "int", type) or self.check_childs(1, "double", type))):
                    raise Exception("Term tail does not agree")
        else:
            return self.get_child_type(0, type)


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
        if self.verify_and_add_token(0, TermNode())\
            and self.verify_and_add_token(1, ExprTailNode()):

                    return True
        else:
            return False

class ExprTailNode(AbstractNode):


    def get_type(self, type):
        if (type == "int" or type == "double") \
                and (self.check_childs(1, "int", type) or self.check_childs(1, "double", type)):
            if len(self.nodes) == 3:
                if not ((self.check_childs(2, "int", type) or self.check_childs(2, "double", type))):
                    raise Exception()
            return self.get_child_type(1, type)
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
        if self.verify_and_add_non_token_node(0, "+")\
            and self.verify_and_add_token(1, TermNode())\
            and self.verify_and_add_token(2, ExprTailNode()):
                    self.option = "+"
                    return True
        elif self.reset()\
                and self.verify_and_add_non_token_node(0, "-") \
                and self.verify_and_add_token(1, TermNode()) \
                and self.verify_and_add_token(2, ExprTailNode()):
                        self.option = "-"
                        return True
        else:
            return None

class TermNode(AbstractNode):

    def get_type(self, type):
        if len(self.nodes) == 3:
            if not (self.check_childs(0, "int", type) or self.check_childs(0, "double", type)) \
                    or not ((self.check_childs(1, "int", type) or self.check_childs(1, "double", type))):
                raise Exception("Term tail does not agree")
            return self.get_child_type(1, type)
        else:
            return self.get_child_type(0, type)
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
        if self.verify_and_add_token(0, UnaryNode())\
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

    def get_type(self, type):
        if (type != "int" or type != "double")\
                and (self.check_childs(1, "int", type) or self.check_childs(1, "double", type)):
            if len(self.nodes) == 3:
                if not ((self.check_childs(2, "int", type) or self.check_childs(2, "double", type))):
                    raise Exception("term tail does not agree")
            return self.get_child_type(1, type)
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

        elif self.reset()\
                and self.verify_and_add_non_token_node(0, "/") \
                and self.verify_and_add_token(1, UnaryNode())\
                and self.verify_and_add_token(2, TermTailNode()):
                    self.option = "/"
                    return True

        else:
            return None

class UnaryNode(AbstractNode):

    def get_type(self, type):
        if self.option == 0:
            if self.nodes[1].get_type(type) == "bool":
                return "bool"

        elif self.option == 1:
            if self.nodes[1].get_type(type) == "int" or self.nodes[1].get_type(type) == "double":
                return self.nodes[1].get_type(type)

        elif self.option == 2:
            return self.nodes[0].get_type(type)
        raise Exception("bad unary type")



    def get_value(self):
        if self.option == 0:
            bool = not self.nodes[1].get_value()
            return bool
        elif self.option == 1:
                return self.nodes[1].get_value() * -1
        elif self.option == 2:
            return self.nodes[0].get_value()


    def name(self):
        return "Unary"

    def parse(self):
        if self.verify_and_add_non_token_node(0, "!")\
            and self.verify_and_add_token(1, UnaryNode()):
                    self.option = 0
                    return True


        elif self.reset()\
                and self.verify_and_add_non_token_node(0, "-") \
                and self.verify_and_add_token(1, UnaryNode()):
                    self.option = 1
                    return True

        elif self.reset()\
            and self.verify_and_add_token(0, FactorNode()):
                    self.option = 2
                    return True
        else:
            return False


class FactorNode(AbstractNode):

    reserved_symbole = {"{", "}", "[", "]", ";", "int", "bool", "char", "double", "=", "True", "False"}

    types = []

    type = ""

    val = None

    def get_Ids(self, list):
        if self.option == 2:
            list.append(True)
            return list
        elif self.option == 0:
            return self.nodes[1].get_Ids(list)
        else:
            return self.nodes[0].get_Ids(list)



    def get_type(self):
        return self.type

    def get_value(self):
        if self.option == 0:
            return self.nodes[1].get_value()
        elif self.option == 1:
            return self.nodes[0].get_value()
        else:
            return self.val

    def get_type(self, type):
        if self.option == 2:
            if type == "bool":
                if "bool" in self.types:
                    self.type = "bool"
                    self.val = bool(self.val)
                    return "bool"
                else:
                    return self.types[0]
            elif type == "int":
                if "int" in self.types:
                    self.val = int(self.val)
                    self.type = "int"
                    return "int"
                else:
                    return self.types[0]
            elif type == "double":
                if "double" in self.types:
                    self.val = float(self.val)
                    self.type = "double"
                    return "double"
                else:
                    return self.types[0]
            else:
                raise Exception("not correct type")
        elif self.option == 0:
            self.type = self.nodes[1].get_type()
            return self.type
        else:
            self.type = self.nodes[0].get_type()
            return self.type


    def name(self):
        return "Factor"

    def parse(self):
        token = self.get_token()
        if token not in self.reserved_symbole:
            if self.verify_and_add_non_token_node(0, "(")\
                and self.verify_and_add_token(1, BoolNode())\
                and self.verify_and_add_non_token_node(2, ")"):
                        self.option = 0
                        return True

            elif self.reset()\
                and not self.is_type() \
                and self.verify_and_add_token(0, LocNode()):
                    self.option = 1
                    return True

            elif self.reset() and self.is_type():
                    #self.nodes.append(GenericNode(self.get_token()))
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


node = ProgramNode()
node.parse()