import ReserveWords
from Tokenizer import Id_Token
from AST import Node
#import Lexer
import unittest

class AST_tester(unittest.TestCase):
    def test_tree(self):
        first_test_tree = Node(Void_token())

# lets test the tokens = [int_token(), number_token(5), id_token(x), equals_token(), semicolon_token()]
# assertEquals(tokens, Node(equals()))

root.print_tree()