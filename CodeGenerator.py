from Productions import*
from ReserveWords import*
from Expressions import*

def with_space(text):
    return text +  ' '

def tab_before_with_space(text, num_tabs = 1):
    return with_space(tab_before(text, num_tabs))

def tab_before(text, num_tabs = 1):
    current_tabs = '    ' * num_tabs
    return current_tabs + text

def comma_vardec(list_comma_vardec): # returns comma vardec as a string in JS format
    vardec = ''

    if len(list_comma_vardec) > 1:
        for i in range(len(list_comma_vardec) - 1):
            comma_vardec = list_comma_vardec[i]
            vardec += with_space(comma_vardec.variable.var_name + ',')
        vardec += list_comma_vardec[len(list_comma_vardec) - 1].variable.var_name
    elif list_comma_vardec:
        vardec += list_comma_vardec[0].variable.var_name

    return vardec

def get_primary_exp(primary):
     match primary:
        case IntLiteral():
            return str(primary.value)
        case BooleanLiteral():
            return str(primary.value)
        case IdExp():
             return primary.name
        case _:
             return str('Error got ' + str(primary))

def op_exp_op(current_exp):
    return get_primary_exp(current_exp.left_exp) + ' ' +  current_exp.op.op_type + ' ' + get_primary_exp(current_exp.right_exp)



def get_exp(exp):
    current_exp = exp.exp

    match current_exp :
        case add_exp():
            return op_exp_op(current_exp)
        case mult_exp():
            return op_exp_op(current_exp)
        case call_exp():
            return op_exp_op(current_exp)
        case IntLiteral():
            return str(current_exp.value)
        case BooleanLiteral():
            return str(current_exp.value)


def get_stmt(stmt):
    match stmt:
        case exp_stmt():
            return get_exp(stmt)
        case vardec_stmt():
            return 'let ' + stmt.variable.var_name
        case assign_stmt():
            return 'let ' + stmt.variable.var_name + ' = ' + get_exp(stmt)
        
        


class CodeGenerator:
    def __init__(self, program):
        self.program = program
        self.classes = program.classes
        self.stmts = program.stmts

    def code_gen(self):
        with open('JS_Code.txt', 'w') as file:
            for class_ in self.classes:

                file.write(with_space('class'))
                file.write(with_space(class_.class_name))
                if class_.extends_name:
                    file.write(with_space('extends ' + class_.extends_name ))
                file.write('{\n')
                num_tabs = 1

                for vardec in class_.vardecs:
                    file.write(tab_before(vardec.variable.var_name + ';\n', num_tabs))

                for constructor in class_.constructors:
                    file.write(tab_before('constructor('))

                    if constructor.comma_vardec: # checks if vardecs list is not empty
                        list_comma_vardec = constructor.comma_vardec.vardecs
                        file.write(comma_vardec(list_comma_vardec))

                    file.write(') {\n')
                    num_tabs+=1

                    list_comma_exp = constructor.comma_exp
                    if list_comma_exp != None:
                        file.write(tab_before('super(', num_tabs))
                        
                        if list_comma_exp: #checks if comma list is not empty
                            if len(list_comma_exp) > 1:
                                for i in range(len(list_comma_exp) - 1):
                                    comma_exp = list_comma_vardec[i]
                                    file.write(with_space(comma_exp.variable.var_name + ','))
                                file.write(list_comma_exp[len(list_comma_exp) - 1].name)
                            elif list_comma_exp:
                                file.write(list_comma_exp[0].name)
                    
                        file.write(');')
                    

                    for stmt in constructor.stmts:  #finish print_stmt function later on line 11
                        file.write(tab_before(get_stmt(stmt), num_tabs))

                    num_tabs -= 1
                    file.write('\n' + tab_before('}\n', num_tabs))
                    
                for method in class_.methods:
                    file.write(tab_before(method.method_name + '(', num_tabs))

                    if method.comma_vardec:
                        list_comma_vardec = method.comma_vardec.vardecs
                        file.write(comma_vardec(list_comma_vardec))

                    num_tabs += 1
                    file.write(') {\n')

                    for stmt in method.stmts:
                        file.write(tab_before(get_stmt(stmt) + ';\n', num_tabs))

                    num_tabs -= 1
                    file.write(tab_before('}\n', num_tabs))                    

                file.write('}\n\n')

            for stmt in self.stmts:
                file.write(get_stmt(stmt) + ';\n')

