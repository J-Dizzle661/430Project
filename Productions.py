

class Production:
    def __init__(self):
        pass

class Type_prod:
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



class Stmt:
    def __init__(self):
        pass

class vardec_stmt(Stmt):
    def __init__(self, type, variable):
        self.type = type
        self.variable = variable
    

class assign_stmt(Stmt):
    def __init__(self, variable, exp):
        self.variable = variable
        self.exp = exp

class while_stmt(Stmt):
    def __init__(self, guard, stmt):
        self.guard = guard #this is the condition
        self.stmt = stmt
        

class break_stmt(Stmt):
    def __init__(self):
        self.stmt = 'break;'

class return_stmt(Stmt):
    def __init__(self, exp):
        self.exp = exp
        

class if_stmt(Stmt):
    def __init__(self, guard, stmt):
        self.guard = guard #this is the condition
        self.stmt = stmt

class else_stmt(Stmt):
    def __init__(self, stmt):
        self.stmt = stmt

class block_stmt(Stmt):
    def __init__(self, stmts):
        self.stmts = stmts

class exp_stmt(Stmt): #might delete
    pass



class Exp:
    pass

class call_exp(Exp):
    pass

class comma_exp(Exp):
    pass

class mult_exp(Exp):
    pass

class add_exp(Exp):
    pass

class primary_exp(Exp):
    pass




class MethodDef:
    pass

class contstructor_method(MethodDef):
    pass



class Variable:
    def __init__(self, var_name):
        self.var_name = var_name



class Class_Def:
    def __init__(self):
        pass

class Program:
    def __init__(self, stmts, classes): #stmts  and class_defs should probably be lists
        self.stmts = stmts
        self.classes = classes

