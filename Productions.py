from Operations import *

class Production:
    def __init__(self):
        pass

def __str__(self):
    return f"BinOpExp({self.left_exp}, {self.op.op_type}, {self.right_exp})"

class Stmt:
    def __init__(self):
        pass

class vardec_stmt(Stmt):
    def __init__(self, type, variable):
        self.type = type
        self.variable = variable

class comma_vardec_stmt(Stmt):  #vardecs should be a list 
    def __init__(self, vardecs):
        self.vardecs = vardecs
    

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
    def __init__(self, guard, then_stmt, else_stmt=None):
        self.guard = guard  # this is the condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

class else_stmt(Stmt):
    def __init__(self, stmts):
        self.stmt = stmts

class block_stmt(Stmt):
    def __init__(self, stmts): #list of stmts
        self.stmts = stmts

class exp_stmt(Stmt):
    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        print("Exp stmt ", self.exp)



class Exp:
    pass

class BinOpExp(Exp):
    def __init__(self, left_exp, op = None, right_exp = None):

        #if ((op == None and right_exp != None) or (op != None and right_exp == None)):
         #   raise Exception('Not a valid Expression')
        
        self.left_exp = left_exp
        self.op = op
        self.right_exp = right_exp


class Type_prod(Exp):
    def __init__(self, value):
        self.value = value

class Int_Type(Type_prod):
    def __init__(self):
        super().__init__('Int')

class Boolean_Type(Type_prod):
    def __init__(self):
        super().__init__('Boolean')

class Void_Type(Type_prod):
    def __init__(self):
        super().__init__('void')

class primary_exp(Exp):
    def __init__(self, left_exp, op=None, right_exp=None):   ## Not sure if necessary, might delete
        super().__init__(left_exp, op, right_exp)
        
class call_exp(BinOpExp):
    def __init__(self, left_exp, right_exp):
        super().__init__(left_exp, DotOp(), right_exp)

class comma_exp():
   def __init__(self, exps): #right could be a list
        self.exps = exps

class mult_exp(BinOpExp):
    def __init__(self, left_exp, op, right_exp): #the op in construct should be a mult_op() or div_op()
        super().__init__(left_exp, op, right_exp)

class add_exp(BinOpExp):
    def __init__(self, left_exp, op, right_exp): #the op in construct should be a plus_op() or minus_op()
        super().__init__(left_exp, op, right_exp)





class MethodDef:
    def __init__(self, method_name, comma_vardec, type, stmts): # comma_vardec object, stmts should be a one or more list
        self.method_name = method_name
        self.comma_vardec = comma_vardec
        self.type = type
        self.stmts = stmts
        

class constructor_method(MethodDef):
    def __init__(self, comma_vardec, comma_exp, stmts):
        super().__init__('init', comma_vardec, Void_Type(), stmts)
        self.comma_exp = comma_exp



class Variable:
    def __init__(self, var_name):
        self.var_name = var_name



class Class_Def:
    def __init__(self, class_name, vardecs, constructors,  methods, extends_name = None):
        self.class_name = class_name
        self.vardecs = vardecs
        self.constructors = constructors
        self.methods = methods
        self.extends_name = extends_name

class Program:
    def __init__(self, classes, stmts = None): #stmts  and class_defs should probably be lists
        self.stmts = stmts
        self.classes = classes

