from Tokenizer import Tokenizer, Id_Token
from ReserveWords import *
from Symbols import *
from Operations import *
from AST import Node
from Productions import *
from dataclasses import dataclass

@dataclass
class ParseResult:
    result: any
    next_pos: int

class Exp(Node):
    pass

@dataclass
class IdExp(Exp):
    name:str

@dataclass
class CallExp(Exp):
    func: IdExp 
    args: list[Exp]

@dataclass
class IntLiteral(Exp):
    value: int

@dataclass
class BooleanLiteral(Exp):
    value: bool

@dataclass
class BinOpExp(Exp):
    left: Exp
    op: Op
    right: Exp

class ParseException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def read_token(self, x):
        if (self.position < 0 or self.position >= len(self.tokens)):
            raise Exception(f"Ran out of tokens")
        else:
          return self.tokens[self.position]
        
    def assert_token_is(self, pos, expected_token):
        actual_token = self.read_token(pos)
        if not isinstance(actual_token, type(expected_token)):
            raise ParseException(
                f"Expected token {type(expected_token).__name__} at position {pos}, "
                f"but found {type(actual_token).__name__}"
        )
    
    def type_parser(self, pos):
        tokens = self.tokens
        if pos >= len(tokens):
            raise ParseException("Expected type but ran out of tokens")
        token = tokens[pos]
        if isinstance(token, Int_Type):
            return ParseResult(Int_Type(), pos + 1)
        elif isinstance(token, Boolean_Type):
            return ParseResult(Boolean_Type(), pos + 1)
        elif isinstance(token, Void_Type):
            return ParseResult(Void_Type(), pos + 1)
        else:
            raise ParseException(f"Expected type at position {pos}, but got: {token}")

    #comma_exp
    def comma_exp(self, start_pos):
        e = self.exp(start_pos+1)
        while self.assert_token_is(e.next_pos, Comma_Token()):
            e.next_pos += 1
            e2 = self.exp(e.next_pos)
            return ParseResult(comma_exp(e.result, e2.result), e2.next_pos)

    def primary_exp(self, start_pos):
        token = self.read_token(start_pos)
        #var
        if isinstance(token, Id_Token):
            return ParseResult(IdExp(token.value), start_pos + 1)
        #int
        elif isinstance(token, Int_token):
            return ParseResult(IntLiteral(token.value), start_pos + 1)
        #this
        elif isinstance(token, this_token):
            return ParseResult(IdExp(token.value), start_pos + 1)
        #true
        elif isinstance(token, true_token):
            return ParseResult(BooleanLiteral(token.value), start_pos + 1)
        #false
        elif isinstance(token, false_token):
            return ParseResult(BooleanLiteral(token.value), start_pos + 1)
        #println
        elif isinstance(token, print_token):
            return ParseResult(IdExp(token.value), start_pos + 1)
        #new
        elif isinstance(token, new_token):
            return ParseResult(IdExp(token.value), start_pos + 1)
        elif isinstance(token, LP_Token):
            e = self.exp(start_pos + 1)
            self.assert_token_is(e.next_pos, RP_Token())
            return ParseResult(e.result, e.next_pos + 1) 
        else:
            raise ParseException(f"Expected primary expression at position: {start_pos}")
        
    #create call_exp
    #call_exp has to call primary_exp
    def call_exp(self, start_pos):
        m = self.primary_exp(start_pos)
        result = m.result
        pos = m.next_pos
        while True:
            try:
                t = self.read_token(pos)
                if isinstance(t, LP_Token):
                    pos += 1
                    args = []
                    if isinstance(self.read_token(pos), RP_Token):
                        pos +=1
                        result = CallExp(result, [])
                        continue
                    args_parse = self.comma_exp(pos)
                    args = args_parse.result
                    pos = args_parse.next_pos
                    self.assert_token_is(pos, RP_Token())
                    pos += 1
                    result = CallExp(result, args)
                else:
                    break
            except ParseException:
                break
        return ParseResult(result, pos)

    def mult_exp(self, start_pos):
        m = self.call_exp(start_pos)
        result = m.result
        should_run = True
        pos = m.next_pos
        while should_run:
            try:
                t= self.read_token(pos)
                if isinstance(t, Star_Token):
                    op = MultOp()
                elif isinstance(t, Div_Token):
                    op = DivOp()
                else: 
                    raise ParseException("Expected * or /")
                m2 = self.call_exp(pos + 1)
                result = BinOpExp(result, op, m2.result)
                pos = m2.next_pos
            except ParseException:
                should_run = False
        return ParseResult(result, pos) #instead of returning parse result it should just call make_node function instead (that will build the tree)

    def add_exp(self, start_pos):
        m = self.mult_exp(start_pos)
        result = m.result
        pos = m.next_pos
        while True:
            try: 
                t = self.read_token(pos)
                if isinstance(t, Plus_Token):
                    op = PlusOp()
                elif isinstance(t, Minus_Token):
                    op = MinusOp()
                else: 
                    raise ParseException("Expected + or -")
                m2 = self.mult_exp(pos+1)
                result = BinOpExp(result, op, m2.result)
                pos = m2.next_pos
            except ParseException:
                break
        return ParseResult(result, pos) 
    
    def exp(self, start_pos):
        return self.add_exp(start_pos)
    
    def vardec_parser(self, pos):
        type_result = self.type_parser(pos)
        id_token = self.read_token(type_result.next_pos)

        if not isinstance(id_token, Id_Token):
            raise ParseException(f"Expected variable name at {type_result.next_pos}")

        var = Variable(id_token.name)
        return ParseResult(vardec_stmt(type_result.result, var), type_result.next_pos + 1)

    def stmt(self, start_pos):
        t = self.read_token(start_pos)

        # vardec
        try:
            type_result = self.type_parser(start_pos)
            id_token = self.read_token(type_result.next_pos)
            if isinstance(id_token, Id_Token):
                self.assert_token_is(type_result.next_pos + 1, SemiColon_Token())
                return ParseResult(
                    vardec_stmt(type_result.result, Variable(id_token.name)),
                    type_result.next_pos + 2
                )
        except ParseException:
            pass

        # assignment
        if isinstance(t, Id_Token):
            next_token = self.read_token(start_pos + 1)
            if isinstance(next_token, Equals_Token):
                e = self.exp(start_pos + 2)
                self.assert_token_is(e.next_pos, SemiColon_Token())
                return ParseResult(assign_stmt(Variable(t.name), e.result), e.next_pos + 1)

        # while stmt
        if isinstance(t, while_token):
            self.assert_token_is(start_pos + 1, LP_Token())
            cond = self.exp(start_pos + 2)
            self.assert_token_is(cond.next_pos, RP_Token())
            body = self.stmt(cond.next_pos + 1)
            return ParseResult(while_stmt(cond.result, body.result), body.next_pos)

        # break stmt 
        if isinstance(t, break_token):
            self.assert_token_is(start_pos + 1, SemiColon_Token())
            return ParseResult(break_stmt(), start_pos + 2)

        # return stmt
        if isinstance(t, return_token):
            next_token = self.read_token(start_pos + 1)
            if isinstance(next_token, SemiColon_Token):
                return ParseResult(return_stmt(Exp()), start_pos + 2)
            else:
                e = self.exp(start_pos + 1)
                self.assert_token_is(e.next_pos, SemiColon_Token())
                return ParseResult(return_stmt(e.result), e.next_pos + 1)

        # if else stmt
        if isinstance(t, if_token):
            self.assert_token_is(start_pos + 1, LP_Token())
            cond = self.exp(start_pos + 2)
            self.assert_token_is(cond.next_pos, RP_Token())
            then_stmt = self.stmt(cond.next_pos + 1)
            pos = then_stmt.next_pos
            try:
                if isinstance(self.read_token(pos), else_token):
                    else_stmt = self.stmt(pos + 1)
                    return ParseResult(if_stmt(cond.result, then_stmt.result, else_stmt.result), else_stmt.next_pos)
            except ParseException:
                pass
            return ParseResult(if_stmt(cond.result, then_stmt.result, None), pos)

        # stmt* 
        if isinstance(t, LSBracket_Token):  # assuming LSBracket_Token = {
            pos = start_pos + 1
            stmts = []
            while not isinstance(self.read_token(pos), RSBracket_Token):  # }
                s = self.stmt(pos)
                stmts.append(s.result)
                pos = s.next_pos
            return ParseResult(block_stmt(stmts), pos + 1)

        # expression stmt
        try:
            e = self.exp(start_pos)
            self.assert_token_is(e.next_pos, SemiColon_Token())
            return ParseResult(exp_stmt(e.result), e.next_pos + 1)
        except ParseException:
            raise ParseException(f"Invalid statement at position {start_pos}")

    def comma_vardec_parser(self, pos):
        vardecs = []
        vd = self.vardec_parser(pos)
        vardecs.append(vd.result)
        pos = vd.next_pos

        while pos < len(self.tokens):
            token = self.read_token(pos)
            if not isinstance(token, Comma_Token):
                break
            pos += 1
            vd = self.vardec_parser(pos)
            vardecs.append(vd.result)
            pos = vd.next_pos

        return ParseResult(vardecs, pos)
    
    def methoddef(self, start_pos):
        pos = start_pos

        token = self.read_token(pos)
        if not isinstance(token, method_token):
            raise ParseException(f"Expected 'method' at position {pos}")
        pos += 1

        token = self.read_token(pos)
        if not isinstance(token, Id_Token):
            raise ParseException(f"Expected method name at position {pos}")
        method_name = token.name
        pos += 1

        self.assert_token_is(pos, LP_Token())
        pos += 1

        params_result = self.comma_vardec_parser(pos)
        params = params_result.result
        pos = params_result.next_pos

        self.assert_token_is(pos, RP_Token())
        pos += 1

        type_result = self.type_parser(pos)
        return_type = type_result.result
        pos = type_result.next_pos

        self.assert_token_is(pos, LSBracket_Token())  # Adjusted to match LSBracket_Token
        pos += 1

        stmts = []
        while not isinstance(self.read_token(pos), RSBracket_Token):
            stmt_result = self.stmt(pos)
            stmts.append(stmt_result.result)
            pos = stmt_result.next_pos

        self.assert_token_is(pos, RSBracket_Token())  # Adjusted to match RSBracket_Token
        pos += 1

        method = MethodDef(method_name, params, return_type, stmts)
        return ParseResult(method, pos)
    
    def constructor(self, pos):
        # 'constructor'
        token = self.read_token(pos)
        if token.value != "constructor":
            raise ParseException(f"Expected 'constructor' at position {pos}")
        pos += 1

        # '('
        self.assert_token_is(pos, LP_Token())
        pos += 1

        # comma_vardec
        params_result = self.comma_vardec_parser(pos)
        comma_vardec = params_result.result
        pos = params_result.next_pos

        # ')'
        self.assert_token_is(pos, RP_Token())
        pos += 1

        # 'super'
        self.assert_token_is(pos, super_token())
        pos += 1

        # '('
        self.assert_token_is(pos, LP_Token())
        pos += 1

        # comma_exp
        comma_exp_result = self.comma_exp(pos)
        super_args = comma_exp_result.result
        pos = comma_exp_result.next_pos

        # ')'
        self.assert_token_is(pos, RP_Token())
        pos += 1

        # '{'
        self.assert_token_is(pos, LSBracket_Token())
        pos += 1

        # parse stmt*
        stmts = []
        while not isinstance(self.read_token(pos), RSBracket_Token()):
            stmt_result = self.stmt(pos)
            stmts.append(stmt_result.result)
            pos = stmt_result.next_pos

        # '}'
        self.assert_token_is(pos, RSBracket_Token())
        pos += 1

        constructor = constructor_method(comma_vardec, super_args, stmts)
        return ParseResult(constructor, pos)

    def classdef(self, pos):
        # 'class'
        token = self.read_token(pos)
        if token.value != "class":
            raise ParseException(f"Expected 'class' at position {pos}")
        pos += 1

        # classname
        token = self.read_token(pos)
        if not isinstance(token, Id_Token):
            raise ParseException(f"Expected class name at position {pos}")
        class_name = token.name
        pos += 1

        # optional 'extends'
        extends_name = None
        if self.read_token(pos).value == "extends":
            pos += 1
            token = self.read_token(pos)
            if not isinstance(token, Id_Token):
                raise ParseException(f"Expected superclass name at position {pos}")
            extends_name = token.name
            pos += 1

        # '{'
        self.assert_token_is(pos, LSBracket_Token())
        pos += 1

        # parse vardec*
        vardecs = []
        while isinstance(self.read_token(pos), (Int_Type, Boolean_Type, Void_Type)):
            vardec_result = self.vardec_parser(pos)
            vardecs.append(vardec_result.result)
            pos = vardec_result.next_pos
            self.assert_token_is(pos, SemiColon_Token())
            pos += 1

        # parse constructor (optional)
        constructors = []
        if self.read_token(pos).value == "constructor":
            constructor_result = self.constructor(pos)
            constructors.append(constructor_result.result)
            pos = constructor_result.next_pos

        # parse methoddef*
        methods = []
        while self.read_token(pos).value == "method":
            method_result = self.methoddef(pos)
            methods.append(method_result.result)
            pos = method_result.next_pos

        # '}'
        self.assert_token_is(pos, RSBracket_Token())
        pos += 1

        return ParseResult(Class_Def(class_name, vardecs, constructors + methods, extends_name), pos)

    def program(self, start_pos=0):
        pos = start_pos
        stmts = []
        classes = []

        while pos < len(self.tokens):
            token = self.read_token(pos)

            # Try to parse a class definition
            if isinstance(token, class_token):
                class_result = self.classdef(pos)
                classes.append(class_result.result)
                pos = class_result.next_pos

            # Try to parse a statement
            else:
                try:
                    stmt_result = self.stmt(pos)
                    stmts.append(stmt_result.result)
                    pos = stmt_result.next_pos
                except ParseException as e:
                    raise ParseException(f"Failed to parse at position {pos}: {e}")

        return ParseResult(Program(classes, stmts), pos)
    
def traverse_exp(exp):
    match(exp):
        case BinOpExp():
            return Node(exp)
        case Int_Type():
            return Node
    
def traverse_stmt():
    pass

'''  
def makeTree(program):
    #do something that takes in a production
    #and spits out a node, which is then added to the AST
    tree = Node(program) 

    for stmt in program.stmts:
        tree.add_child(Node(stmt))

    for cls in program.classes:
        tree.add_child(Node(cls))

        for vardec in cls.vardecs:
            cls.add_child(Node(vardec))

        for method in cls.methods:
            cls.addchild(Node(method))
            case(primary_exp()):
            pass


        

    tree.print_tree()
       


    tree.print_tree()
  '''     

