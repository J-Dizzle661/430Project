from Lexer.Tokenizer import Tokenizer
from Lexer.Token import Token
from Lexer.ReserveWords import ReserveWord
from AST import Node

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def read_token(self):
        if (self.position < 0 or self.position >= len(self.tokens)):
            raise Exception(f"Ran out of tokens")
        else:
          return self.tokens[self.position]
        
    def primary_exp (self):
        token = self.read_token()

        if isinstance(token, ReserveWord.Int_Token):
            self.position += 1 
            return Node(token)
        
        elif isinstance(token, ReserveWord.Id_Token):
            self.position += 1 
            return Node(token)
        
        elif isinstance(token, ReserveWord.this_Token):
            self.position += 1 
            return Node(token)

        elif isinstance(token, ReserveWord.true_Token):
            self.position += 1 
            return Node(token)
        
        elif isinstance(token, ReserveWord.false_Token):
            self.position += 1 
            return Node(token)
        
        elif isinstance(token, ReserveWord.println_Token):
            self.position += 1 
            return Node(token)
        
        elif isinstance(token, ReserveWord.new_Token):
            self.position += 1 
            return Node(token)
        
        raise Exception(f"Token Unexpected: {token}")