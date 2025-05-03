from typing import Optional
from Token import Token
import Operations as op
import Symbols as symb
import ReserveWords as res
    
class Id_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class IntLiteral_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class Tokenizer(Token):
    def __init__(self, input_str):
        self.input = input_str
        self.position = 0
        self.symbol_map = {
            "(": symb.LP_Token,
            ")": symb.RP_Token,
            "[": symb.LBracket_Token,
            "]": symb.RBracket_Token,
            "}": symb.RSBracket_Token,
            "{": symb.LSBracket_Token,
            ";": symb.SemiColon_Token,
            ",": symb.Comma_Token,
            ":": symb.Colon_Token,
            "=>": symb.Arrow_Token,
            "*": symb.Star_Token,
            "/": symb.Div_Token,
            "=": symb.Equals_Token,
            "+": symb.Plus_Token,
            "-": symb.Minus_Token,
            '.': symb.Dot_Token,
            '<': symb.Less_Than_Token,
            '>': symb.Greater_Than_Token,
            '&&': symb.Add_Token,
            '||': symb.Or_Token,
        }

    def get_position(self) :
        return self.position
    
    def skip_whitespace(self):
        while self.position < len(self.input) and self.input[self.position].isspace():
            self.position += 1

    #def try_read_op_token(self) :
       # if (self.input).startswith(Int_Token, self.position) and 

    def try_read_number_token(self) :
        digits = ""

        while self.position < len(self.input) and self.input[self.position].isdigit():
            digits += self.input[self.position]
            self.position += 1

        if not digits:
            return None
        return IntLiteral_Token(int(digits))
    
    def try_read_ID_Or_Reserve_Token(self):
        if self.position < len(self.input) and self.input[self.position].isalpha():
            chars = self.input[self.position]
            self.position += 1
            while self.position < len(self.input) and self.input[self.position].isalnum():
                chars += self.input[self.position]
                self.position += 1

            reserved_map = {
                "println": res.print_token,
                "this": res.this_token,
                "true": res.true_token,
                "false": res.false_token,
                "new": res.new_token,
                "while": res.while_token,
                "break": res.break_token,
                "return": res.return_token,
                "if": res.if_token,
                "else": res.else_token,
                "method": res.method_token,
                "init": res.init_token,
                "super": res.super_token,
                "class": res.class_token,
                "Int": res.Int_token,
                "Boolean": res.Boolean_token,
                "Void": res.Void_token,
                "extends": res.extends_token,
            }

            if chars in reserved_map:
                return reserved_map[chars]()
            else:
                return Id_Token(chars)
        return None

        
    def try_read_symbol(self):
        for symbol in sorted(self.symbol_map.keys(), key=len, reverse=True): 
            if self.input.startswith(symbol, self.position):
                self.position += len(symbol)
                return self.symbol_map[symbol]()  
        return None

    def read_Tokens(self) :
        list_tokens = []
        while True:
            self.skip_whitespace()
            if self.position >= len(self.input):
                break
            token = self.try_read_number_token()
            if token is None:
                token = self.try_read_symbol()
            if token is None:
                token = self.try_read_ID_Or_Reserve_Token()
            if token is None:
                current_char = self.input[self.position] if self.position < len(self.input) else "<EOF>"
                context = self.input[self.position:self.position + 10] if self.position < len(self.input) else "<EOF>"
                raise Exception(
                    f"\nInvalid Token!\n"
                    f"Char: '{current_char}' at position {self.position}\n"
                    f"Context: '{context}'\n"
                )
            else:
                list_tokens.append((token))
        return list_tokens
    
      ## Might impliment this later to make testing easier and faster -Jason ##
    
        