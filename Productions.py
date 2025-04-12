from AST import Node_Type

class Int_node(Node_Type):
    def __init__(self, value):
        super().__init__(value)

class Boolean_node(Node_Type):
    def __init__(self, value):
        super().__init__(value)

class Void_node(Node_Type):
    def __init__(self):
        super().__init__('void')