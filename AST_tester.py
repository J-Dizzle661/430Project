import ReserveWords
from Tokenizer import Id_Token
from AST import Node
#import Lexer
import unittest

class AST_tester(unittest.TestCase):
    def test_tree(self):
        first_test_tree = Node(Void_token())

root = Node(ReserveWords.Boolean_token())
some_child = Node(ReserveWords.break_token())
root.add_child(some_child)
other_child = Node(ReserveWords.false_token())
root.add_child(Node(ReserveWords.this_token()))
root.add_child(other_child)
some_child.add_child(Node(ReserveWords.print_token()))
some_child.add_child(Node(ReserveWords.Void_token()))
some_child.add_child(Node(ReserveWords.method_token()))
other_child.add_child(Node(ReserveWords.new_token()))
other_child.add_child(Node(Id_Token('Yeah Buddy')))

root.print_tree()