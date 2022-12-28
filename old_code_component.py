"""
Create nodes + parse tree using grammar:

   <program>  ::= <block>
   <block>    ::= { <decls> <stmts> }
   <decls>    ::= e
                | <decl> <decls>
   <decl>     ::= <type> ID ;
   <type>     ::= BASIC
   <stmts>    ::= e
                | <stmt> <stmts>
   <stmt>     ::= <loc> = <bool> ;
                | IF ( <bool> ) <stmt>
                | IF ( <bool> ) <stmt> ELSE <stmt>
                | WHILE ( <bool> ) <stmt>
                | <block>
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


def turn_right():
    pass


def turn_left():
    pass


def go_forward():
    pass


def can_go_forward():
    pass

    """
    rover keyword is essentially a dumb value to be used with commands to make the rover do stuff and increase 
    code legibility ex: rover = goRight. the value assignment does basically nothing since all commands simply 
    return None, therefore to get access to values in and out, we use the system values which are changed when 
    calling the values
    """


GLOBAL_SCOPE = {
    "rover": {"value": None, "type": "rover"}
    , "systemInt": {"value": 0, "type": "int"}
    , "systemBool": {"value": False, "type": "bool"}
    , "goRight": {"value": go_right(), "type": "rover"}
    , "goUp": {"value": go_up(), "type": "rover"}
    , "goLeft": {"value": go_left(), "type": "rover"}
    , "goDown": {"value": go_down(), "type": "rover"}
    , "canGoRight": {"value": can_go_right(), "type": "rover"}
    , "canGoUp": {"value": can_go_up(), "type": "rover"}
    , "canGoLeft": {"value": can_go_left(), "type": "rover"}
    , "canGoDown": {"value": can_go_down(), "type": "rover"}
    , "getGround": {"value": get_ground(), "type": "rover"}
    , "setGround": {"value": set_ground(), "type": "rover"}
    , "dig": {"value": dig(), "type": "rover"}
    , "turnRight": {"value": turn_right(), "type": "rover"}
    , "turnLeft": {"value": turn_left(), "type": "rover"}
    , "canGoForward": {"value": can_go_forward(), "type": "rover"}
    , "goForward": {"value": go_forward(), "type": "rover"}

}
