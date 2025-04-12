from Tokenizer import Tokenizer, Id_Token
from ReserveWords import Int_token
from Symbols import LP_Token, RP_Token
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
        token = self.get_token(start_pos)
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