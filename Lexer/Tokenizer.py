from typing import Optional


class Token() :
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"
    
class Div_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class Equals_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class Id_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class Int_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class LP_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class RP_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class Minus_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class Plus_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class Print_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class SemiC_Token(Token) :
    def __init__(self, value):
        super().__init__(value)

class Star_Token(Token) :
    def __init__(self, value):
        super().__init__(value)


class Tokenizer(Token):
    def __init__(self, input_str):
        self.input = input_str
        self.position = 0

    def get_position(self) :
        return self.position
    
    def skip_whitespace(self):
        while self.position < len(self.input) and self.input[self.position].isspace():
            self.position += 1

    #def try_read_op_token(self) :
       # if (self.input).startswith(Int_Token, self.position) and 

    def try_read_int_token(self) -> Optional[Token]:
        digits = ""

        while self.position < len(self.input) and self.input[self.position].isdigit():
            digits += self.input[self.position]
            self.position += 1

        if not digits:
            return None
        return Int_Token(int(digits))
    
    def try_read_ID_Token(self) -> Optional[Token]:
        if self.position < len(self.input) and self.input[self.position].isalpha() :
            chars = "" + self.input[self.position]
            self.position += 1
            while self.position < len(self.input) and self.input[self.position].isalnum() :
                chars += self.input[self.position]
                self.position += 1
            if chars == "print" :
                return Print_Token
            else :
                return Id_Token
        else :
            return None
        
    def try_read_symbol(self) -> Optional[Token] :
        if (self.input).startswith("(", self.position) :
            self.position += 1
            return LP_Token
        elif (self.input).startswith(")", self.position) :
            self.position += 1
            return RP_Token
        else :
            return None

    def read_Token(self) :
        self.skip_whitespace()
        token = self.try_read_int_token()
        if token is None :
            token = self.try_read_symbol()
        if token is None :
            token = self.try_read_ID_Token()
        if token is None :
            raise Exception(f"Invalid Token. Expected: (, ), /, *, etc... Got: '{self.input[self.position:]}' at position {self.position}")
        
        return token