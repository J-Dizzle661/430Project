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

def get_comma_exp(exps):
    return_str = ''
    for exp in exps:
        return_str += (get_exp(exp) + ', ')

    return f'{return_str[:len(return_str) - 2]}'  

def get_primary_exp(primary):
     match primary:
        case IntLiteral():
            return str(primary.value)
        case BooleanLiteral():
            return str(primary.value).lower()
        case IdExp():
             return primary.name
        case _:
             return str('Error got ' + str(primary))

def op_exp_op(current_exp):
    return get_primary_exp(current_exp.left_exp) + ' ' +  current_exp.op.op_type + ' ' + get_primary_exp(current_exp.right_exp)



def get_exp(exp):
    match exp :
        case add_exp():
            return op_exp_op(exp)
        case mult_exp():
            return op_exp_op(exp)
        case call_exp():
            if get_exp(exp.left_exp) == 'this':
                return f'{get_exp(exp.left_exp)}{exp.op.op_type}{exp.right_exp[0].name}' 
            else:
                return f'{get_exp(exp.left_exp)}{exp.op.op_type}{exp.right_exp[0].name}({get_comma_exp(exp.right_exp[1:])})'
        case IntLiteral():
            return str(exp.value)
        case BooleanLiteral():
            return str(exp.value)
        case StringLiteral():
            return f'"{exp.value}"'
        case BinOpExp():
            return f"{get_exp(exp.left_exp)} {exp.op.op_type} {get_exp(exp.right_exp)}"
        case IdExp():
            return exp.name
        case ParenExp():
            return f"({get_exp(exp.inner)})"
        case CallExp():
            if isinstance(exp.func, IdExp):
                if exp.func.name == "new":
                    class_name = get_exp(exp.args[0])
                    args = ', '.join(get_exp(arg) for arg in exp.args[1:])
                    return f"new {class_name}({args})"
                elif exp.func.name == "println":
                    args = ', '.join(get_exp(arg) for arg in exp.args)
                    return f"console.log({args})"
            args = ', '.join(get_exp(arg) for arg in exp.args)
            return f"{get_exp(exp.func)}({args})"

def get_stmt(stmt, num_tabs=1):
    match stmt:
        case exp_stmt():
            return get_exp(stmt.exp)
        case vardec_stmt():
            return 'let ' + stmt.variable.var_name
        case assign_stmt():
            if getattr(stmt, 'from_this', False):
                return 'this.' + stmt.variable.var_name + ' = ' + get_exp(stmt.exp)
            else:
                return stmt.variable.var_name + ' = ' + get_exp(stmt.exp)
        case while_stmt():
            return f"while ({get_exp(stmt.guard)}) " + get_stmt(stmt.stmt, num_tabs + 1)
        case block_stmt():
            return '{\n' + '\n'.join(tab_before(get_stmt(s, num_tabs + 1)) + ';' for s in stmt.stmts) + '\n' + tab_before('}', num_tabs)
        case break_stmt():
            return 'break'
        case return_stmt():
            return 'return ' + get_exp(stmt.exp) if stmt.exp else 'return'
        case if_stmt():
            if isinstance(stmt.then_stmt, block_stmt):
                    then_js = get_stmt(stmt.then_stmt, num_tabs)
            else:
                then_body = get_stmt(stmt.then_stmt, num_tabs + 1)
                then_lines = then_body.splitlines()
                then_js = "{\n" + '\n'.join(tab_before(line, num_tabs + 1) for line in then_lines) + "\n" + tab_before("}", num_tabs + 1)

            js_lines = [f"if ({get_exp(stmt.guard)}) {then_js}"]

            if stmt.else_stmt:
                if isinstance(stmt.else_stmt, block_stmt):
                    else_js = get_stmt(stmt.else_stmt, num_tabs)
                else:
                    else_body = get_stmt(stmt.else_stmt, num_tabs + 1)
                    else_lines = else_body.splitlines()
                    else_js = "{\n" + '\n'.join(tab_before(line, num_tabs + 1) for line in else_lines) + "\n" + tab_before("}", num_tabs + 1)
                js_lines.append(f"else {else_js}")

            return '\n'.join(js_lines)

class CodeGenerator:
    def __init__(self, program):
        self.program = program
        self.classes = program.classes
        self.stmts = program.stmts

    def code_gen(self):
        with open('JS_Code.js', 'w') as file:
            for class_ in self.classes:

                file.write(with_space('class'))
                file.write(with_space(class_.class_name))
                if class_.extends_name:
                    file.write(with_space('extends ' + class_.extends_name ))
                file.write('{')
                num_tabs = 1

                for vardec in class_.vardecs:
                    file.write('\n')
                    file.write(tab_before(vardec.variable.var_name + ';', num_tabs))

                for constructor in class_.constructors:
                    file.write('\n')
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
                    
                    for stmt in constructor.stmts:
                        file.write(tab_before(get_stmt(stmt, num_tabs), num_tabs) + ';\n')

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
                        js = get_stmt(stmt, num_tabs)
                        if not js.strip().startswith(('if', 'while', 'for', 'else', '{')):
                            js += ';'
                        for line in js.splitlines():
                            file.write(tab_before(line + '\n', num_tabs))
                    num_tabs -= 1 
                    file.write(tab_before('}\n', num_tabs))                  

                file.write('}\n\n')

            for stmt in self.stmts:
                js = get_stmt(stmt, 0)
                if not js.strip().startswith(('if', 'while', 'for', 'else', '{')):
                    js += ';'
                file.write(js + '\n')

