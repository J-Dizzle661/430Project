from ReserveWords import Void_token
from AST import Node
#import Lexer
import unittest

class AST_tester(unittest.TestCase):
    def test_tree(self):
        first_test_tree = Node(Void_token())