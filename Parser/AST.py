from Token import Token 

class AST:
    def __init__(self):
        pass

class Node:
    def __init__(self, token):
        self.token = token
        self.parent = None
        self.children = []

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"

    def add_child(self, child):
        if instanceof(child, Token):
            self.children.append(child)
            child.parent = self
        else:
            raise Exception('Tried adding ', child.__str__(), ' to ' ,self.__str__(), ' but not a vaild AST Node!')