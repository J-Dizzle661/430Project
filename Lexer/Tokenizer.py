from typing import Optional
from Token import Token
import Operations as op
import Symbols as symb
import ReserveWords as res
    
class Id_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class Int_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

'''  # Moving to Reserve Words file  -Jason
class Print_Token(Token) :     
    def __init__(self, value):
        super().__init__(value)'
'''

class Tokenizer(Token):
    def __init__(self, input_str):
        self.input = input_str
        self.position = 0
        self.symbol_map = {
            "(": symb.LP_Token,
            ")": symb.RP_Token,
            "[": symb.LBracket_Token,
            "]": symb.RBracket_Token,
            "{": symb.RSBracket_Token,
            "}": symb.LSBracket_Token,
            ";": symb.SemiColon_Token,
            ",": symb.Comma_Token,
            ":": symb.Colon_Token,
            "=>": symb.Arrow_Token,
            "*": symb.Star_Token,
            "/": symb.Div_Token,
            "=": symb.Equals_Token,
            "+": symb.Plus_Token,
            "-": symb.Minus_Token,
        }

    def get_position(self) :
        return self.position
    
    def skip_whitespace(self):
        while self.position < len(self.input) and self.input[self.position].isspace():
            self.position += 1

    #def try_read_op_token(self) :
       # if (self.input).startswith(Int_Token, self.position) and 

    def try_read_int_token(self) :
        digits = ""

        while self.position < len(self.input) and self.input[self.position].isdigit():
            digits += self.input[self.position]
            self.position += 1

        if not digits:
            return None
        return Int_Token(int(digits))
    
    def try_read_ID_Or_Reserve_Token(self) :
        if self.position < len(self.input) and self.input[self.position].isalpha() :
            chars = "" + self.input[self.position]
            self.position += 1
            while self.position < len(self.input) and self.input[self.position].isalnum() :
                chars += self.input[self.position]
                self.position += 1
            if chars == "println" :
                return res.print_token()
            elif chars == 'this' :
                return res.this_token()
            elif chars == 'true' :
                return res.true_token()
            elif chars == 'false' :
                return res.false_token()
            elif chars == 'new' :
                return res.new_token()
            elif chars == 'while' :
                return res.while_token()
            elif chars == 'break' :
                return res.break_token()
            elif chars == 'return' :
                return res.return_token()
            elif chars == 'if' :
                return res.if_token()
            elif chars == 'else' :
                return res.else_token()
            elif chars == 'method' :
                return res.method_token()
            elif chars == 'init' :
                return res.init_token()
            elif chars == 'super' :
                return res.super_token()
            elif chars == 'class' :
                return res.this_token()
            elif chars == 'Int' :
                return res.Int_token()
            elif chars == 'Boolean' :
                return res.Boolean_token()
            elif chars == 'Void' :
                return res.Void_token()            
            else :
                return Id_Token(chars)
        else :
            return None
        
    def try_read_symbol(self):
        for symbol in sorted(self.symbol_map.keys(), key=len, reverse=True): 
            if self.input.startswith(symbol, self.position):
                self.position += len(symbol)
                return self.symbol_map[symbol]()  
        return None

    def read_Token(self) :
        self.skip_whitespace()
        token = self.try_read_ID_Or_Reserve_Token()
        if token is None :
            token = self.try_read_symbol()
        if token is None :
            token = self.try_read_ID_Token()
        if token is None :
            raise Exception(f"Invalid Token. Expected: (, ), /, *, etc... Got: '{self.input[self.position:]}' at position {self.position}")
        return token
    
    def tokenize(self):
        list_tokens = []
        while (self.get_position < len(self.input)):
            self.skip_whitespace()
            token = self.try_read_int_token()
            if token is None :
                token = self.try_read_symbol()
            if token is None :
                token = self.try_read_ID_Or_Reserve_Token()
            if token is None :
                raise Exception("Invalid Token. Expected: (, ), /, *, etc... Got: " + self)
            else:
                list_tokens.append(token)
        return list_tokens