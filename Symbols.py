from Token import Token

class Symbol(Token):
    def __init__(self, value) :
        super().__init__(value)

class LP_Token(Symbol):
    def __init__(self):
        super().__init__("(")

class RP_Token(Symbol):
    def __init__(self):
        super().__init__(")")

class RBracket_Token(Symbol):
    def __init__(self):
        super().__init__("[")

class LBracket_Token(Symbol):
    def __init__(self):
        super().__init__("]")

class RSBracket_Token(Symbol):
    def __init__(self):
        super().__init__("{")

class LSBracket_Token(Symbol):
    def __init__(self):
        super().__init__("}")

class SemiColon_Token(Symbol):
    def __init__(self):
        super().__init__(";")

class Comma_Token(Symbol):
    def __init__(self):
        super().__init__(",")

class Colon_Token(Symbol):
    def __init__(self):
        super().__init__(":")

class Arrow_Token(Symbol):
    def __init__(self):
        super().__init__("=>")

class Star_Token(Symbol):
    def __init__(self):
        super().__init__("*")

class Div_Token(Symbol):
    def __init__(self):
        super().__init__("/")

class Plus_Token(Symbol):
    def __init__(self):
        super().__init__("+")

class Minus_Token(Symbol):
    def __init__(self):
        super().__init__("-")

class Equals_Token(Symbol):
    def __init__(self):
        super().__init__("=")

class Dot_Token(Symbol):
    def __init__(self):
        super().__init__('.')

class Less_Than_Token(Symbol):
    def __init__(self):
        super().__init__('<')

class Greater_Than_Token(Symbol):
    def __init__(self):
        super().__init__('>')

class Add_Token(Symbol):
    def __init__(self):
        super().__init__('&&')

class Or_Token(Symbol):
    def __init__(self):
        super().__init__('||')