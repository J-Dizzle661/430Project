from AST import Node_Type

class Production:
    def __init__(self):
        pass

class Type_prod(Production):
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Int_Type(Type_prod):
    def __init__(self, value):
        super().__init__(self, value)

class Boolean_Type(Type_prod):
    def __init__(self, value):
        super().__init__(self, value)

class Void_Type(Type_prod):
    def __init__(self):
        super().__init__(self, 'Void')

class Exp_prod(Production):
    def __init__(self, add_exp):
        self.add_exp = add_exp

class Add_Exp_prod(Production):
    pass

class Vardec(production):
    def __init__(self):
        pass

