from Token import Token


''' Probably gonna delete this later, not useful
class Node_Type:
    def __init__(self, value):
        self.value = value
'''
        

#Dewey advised against a node class:
#The problems with this is because if you see a node object, its harder to work with
# Preffered:
# class Plus_Node, class Int_Literal:

class Node:
    def __init__(self, production):
        self.value = production
        self.parent = None
        self.children = []

    def __str__(self):
        return f"{self.token.__class__.__name__}({self.token.value})"

    def add_child(self, child):
        if isinstance(child.token, Token):
            self.children.append(child)
            child.parent = self
        else:
            raise Exception('Tried adding ' + child.__str__() + ' to '+ self.__str__() +  ' but not a vaild AST Node!')
        
    def print_tree(self):
        for i in range(self.get_level()):
            print('     ', end='')
        if not self.parent:
            print(self.__str__())
        else:
            print('|__', self.__str__())
        if self.children:
            for child in self.children:
                child.print_tree()

    def get_level(self):
        if self.parent:
            return 1 + self.parent.get_level()
        else:
            return 0

    