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
    
    def read_token(self):
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

    def type_parser(tokens, pos):
        if pos >= len(tokens):
            raise ParseException("Expected type but ran out of tokens")
        token = tokens[pos]
        if isinstance(token, Int_token):
            return ParseResult(Int_Type("Int"), pos + 1)
        elif isinstance(token, Boolean_token):
            return ParseResult(Boolean_Type("Boolean"), pos + 1)
        elif isinstance(token, Void_token):
            return ParseResult(Void_Type(), pos + 1)
        else:
            raise ParseException(f"Expected type at position {pos}, but got: {token}")
            
    def primary_exp(self, start_pos):
        token = self.read_token(start_pos)
        if isinstance(token, Id_Token):
            return ParseResult(IdExp(token.name), start_pos + 1)
        elif isinstance(token, Int_token):
            return ParseResult(IntLiteral(token.value), start_pos + 1)
        elif isinstance(token, LP_Token):
            e = self.exp(start_pos + 1)
            self.assert_token_is(e.next_pos, RP_Token())
            return ParseResult(e.result, e.next_pos + 1)
        else:
            raise ParseException(f"Expected primary expression at position: {start_pos}")

    def mult_exp(self, start_pos):
        m = self.primary_exp(start_pos)
        result = m.result
        should_run = True
        pos = m.next_pos
        while should_run:
            try:
                t= self.read_token_token(pos)
                if isinstance(t, Star_Token):
                    op = MultOp()
                elif isinstance(t, Div_Token):
                    op = DivOp()
                else: 
                    raise ParseException("Expected * or /")
                m2 = self.primary_exp(pos + 1)
                result = BinOpExp(result, op, m2.result)
                pos = m2.next_pos
            except ParseException:
                should_run = False
        return ParseResult(result, pos)

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
                return ParseResult(return_stmt(None), start_pos + 2)
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
        # First vardec
        vd = self.vardec_parser(pos)
        vardecs.append(vd.result)
        pos = vd.next_pos

        while pos < len(self.tokens):
            token = self.read_token(pos)
            if not isinstance(token, Comma_Token):
                break  # End of comma list
            pos += 1  # skip comma
            vd = self.vardec_parser(pos)
            vardecs.append(vd.result)
            pos = vd.next_pos
        return ParseResult(vardecs, pos)
    
    '''
def parse_tokens(tokens): # will be some if-else or pattern match to call each appropriate try_parse function below:
    current_postion =0               # this will keep track of position in token list

def try_parse_Exp(): # can return a call exp, comma exp, mult exp, add exp
    try_parse_add_exp()            # or int literal, bool literal, or void  

def try_parse_Stmt():# can return any kind of stmt
    pass

def try_parse_Method(): # can return either a method_def or an an constructor_method
    pass

def try_parse_class_def(): # just returns a class_def
    pass

def make_program(): # adds all the class_defs and stmts
    pass

    '''
def makeTree(program):
    #do something that takes in a production
    #and spits out a node, which is then added to the AST

    program.stmts
    program.class_defs
    for cls in class_defs:
        

    
    match(someProduction):
        case(Exp()):
            match(someProduction):
                case(add_exp()):
                    pass

                case(mult_exp()):
                    pass

                case(call_exp()):
                    pass

                case(primary_exp()):
                    pass


        