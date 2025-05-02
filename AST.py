from Token import Token
from Expressions import Exp, IdExp, CallExp, IntLiteral, BooleanLiteral

class Node:
    def __init__(self, production):
        self.value = production
        self.parent = None
        self.children = []

    def __str__(self):
        return self._format_value()

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def to_string(self, prefix="", is_last=True):
        lines = []
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{self._format_value()}")

        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(self.children):
            is_last_child = (i == len(self.children) - 1)
            lines.append(child.to_string(child_prefix, is_last_child))

        return "\n".join(lines)

    def _format_value(self):
        value = self.value
        name = self.value.__class__.__name__

        if isinstance(value, IdExp):
            return f"{name}({value.name})"
        if isinstance(value, BooleanLiteral):
            return f"{name}({value.value})"
        if isinstance(value, IntLiteral):
            return f"{name}({value.value})"
        if isinstance(value, CallExp):
            return f"{name}()"

        if hasattr(value, "class_name"):
            return f"{name}({value.class_name})"
        if hasattr(value, "method_name"):
            return f"{name}({value.method_name})"
        if hasattr(value, "var_name"):
            return f"{name}({value.var_name})"
        elif hasattr(value, "value") and not isinstance(value.value, (list, Node)):
            return f"{name}({value.value})"
        elif hasattr(value, "name"):
            return f"{name}({value.name})"
        else:
            return f"{name}()"   
        
    def print_tree(self):
        print(self.to_string())

    def get_level(self):
        if self.parent:
            return 1 + self.parent.get_level()
        else:
            return 0

    