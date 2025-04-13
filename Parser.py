from Tokenizer import Tokenizer, Id_Token
from ReserveWords import Int_token
from Symbols import LP_Token, RP_Token, Star_Token, Div_Token, Plus_Token, Minus_Token
from Operations import Op, MultOp, DivOp, PlusOp, MinusOp
from AST import Node
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
class IntExp(Exp):
    value: int

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
        
    def primary_exp(self, start_pos):
        token = self.read_token(start_pos)
        if isinstance(token, Id_Token):
            return ParseResult(IdExp(token.name), start_pos + 1)
        elif isinstance(token, Int_token):
            return ParseResult(IntExp(token.value), start_pos + 1)
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