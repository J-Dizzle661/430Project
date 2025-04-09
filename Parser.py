from Tokenizer import Tokenizer, Int_Token
from Token import Token
from ReserveWords import true_token, false_token, print_token, new_token, this_token, Int_token
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

        if isinstance(token, Int_token):
            self.position += 1 
            return Node(token)
        
        elif isinstance(token, this_token):
            self.position += 1 
            return Node(token)

        elif isinstance(token, true_token):
            self.position += 1 
            return Node(token)
        
        elif isinstance(token, false_token):
            self.position += 1 
            return Node(token)
        
        elif isinstance(token, print_token):
            self.position += 1 
            return Node(token)
        
        elif isinstance(token, new_token):
            self.position += 1 
            return Node(token)
        
        raise Exception(f"Token Unexpected: {token}")