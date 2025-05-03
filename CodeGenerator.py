def with_space(text):
    return text +  ' '

def tab_before_with_space(text, num_tabs = 1):
    current_tabs = ''

    for tabs in num_tabs:
        current_tabs += tabs
    
    return current_tabs + with_space(text)

def tab_before(text):
    return '    ' + text

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
                file.write(class_.class_name + '{\n')

                for vardec in class_.vardecs:
                    file.write(tab_before(vardec.variable.var_name) + ';\n')

                for constructor in class_.constructors:
                    file.write(tab_before('constructor ('))

                    for comma_vardec in constructor.comma_vardec:
                        file.write(with_space(comma_vardec + ','))
                    file.write(') {')

                    if len(constructor.comma_exp) > 0:
                        file.write('super(')
                        
                        for comma_exp in constructor.comma_exp:
                            file.write(with_space(comma_exp + ','))
                    
                    file.write(');')
                    

                    for stmt in constructor.stmts:
                        file.write(tab_before(print_stmt(stmt)))

                    file.write('}')
                    
                    #continue with method def


                    file.write('}')

