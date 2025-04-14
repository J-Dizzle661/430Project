class Op:
    def __init__(self, op_type):
        self.op_type = op_type

class DivOp(Op):
    def __init__(self):
        super().__init__('/')

class MinusOp(Op):
    def __init__(self):
        super().__init__('-')

class MultOp(Op):
    def __init__(self):
        super().__init__('*')

class PlusOp(Op):
    def __init__(self):
        super().__init__('+')

class DotOp(Op):
    def __init__(self):
        super().__init__('.')

class Comma_Op(Op):
    def __init__(self):
        super().__init__(',')

