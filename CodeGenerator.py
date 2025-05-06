def with_space(text):
    return text +  ' '

def tab_before_with_space(text, num_tabs = 1):
    return with_space(tab_before(text, num_tabs))

def tab_before(text, num_tabs = 1):
    current_tabs = '    ' * num_tabs
    return current_tabs + text

def print_stmt(stmt):
    pass   

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
                        if len(list_comma_vardec) > 1:
                            for i in range(len(list_comma_vardec) - 1):
                                comma_vardec = list_comma_vardec[i]
                                file.write(with_space(comma_vardec.variable.var_name + ','))
                            file.write(list_comma_vardec[len(list_comma_vardec) - 1].variable.var_name)
                        elif list_comma_vardec:
                            file.write(list_comma_vardec[0].variable.var_name)
                            
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
                        file.write(tab_before(print_stmt(stmt), num_tabs))

                    num_tabs -= 1
                    file.write('\n' + tab_before('}', num_tabs))
                    
                    #continue with method def


                    file.write('\n}')

