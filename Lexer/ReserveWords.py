from Tokenizer import Token

class ReserveWord(Token):
    def __init__(self, value):
        super().__init__(value)

class this_token(ReserveWord):
    def __init__(self):
        super().__init__('this')

class true_token(ReserveWord):
    def __init__(self):
        super().__init__('true')

class false_token(ReserveWord):
    def __init__(self):
        super().__init__('false')

class print_token(ReserveWord):
    def __init__(self):
        super().__init__('println')

class new_token(ReserveWord):
    def __init__(self):
        super().__init__('new')

class while_token(ReserveWord):
    def __init__(self):
        super().__init__('while')

class break_token(ReserveWord):
    def __init__(self):
        super().__init__('break')

class return_token(ReserveWord):
    def __init__(self):
        super().__init__('return')

class if_token(ReserveWord):
    def __init__(self):
        super().__init__('if')

class else_token(ReserveWord):
    def __init__(self):
        super().__init__('else')

class method_token(ReserveWord):
    def __init__(self):
        super().__init__('method')

class init_token(ReserveWord):
    def __init__(self):
        super().__init__('init')

class super_token(ReserveWord):
    def __init__(self):
        super().__init__('super')

class class_token(ReserveWord):
    def __init__(self):
        super().__init__('class')

class Int_token(ReserveWord):
    def __init__(self):
        super().__init__('Int')

class Boolean_token(ReserveWord):
    def __init__(self):
        super().__init__('Boolean')

class Void_token(ReserveWord):
    def __init__(self):
        super().__init__('Void')