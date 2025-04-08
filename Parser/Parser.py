from Lexer.Tokenizer import Tokenizer
from Lexer.Token import Token

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def read_token(self):
        if (self.position < 0 or self.position >= len(self.tokens)):
            raise Exception(f"Ran out of tokens")
        else:
          return self.tokens[self.position]
        
    
