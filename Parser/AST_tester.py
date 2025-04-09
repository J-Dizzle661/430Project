from Parser.AST import Node
from Lexer.ReserveWords import Void_token
import unittest

class AST_tester(unittest.TestCase):
    def test_tree(self):
        first_test_tree = Node(Void_token())