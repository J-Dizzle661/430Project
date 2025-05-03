import unittest
from Tokenizer import Tokenizer
from Parser import Parser, makeTree
from Productions import assign_stmt, vardec_stmt, while_stmt, if_stmt, return_stmt
from CodeGenerator import *


test_input ='''
            class Animal{
                init(){super();}
            }
            '''

tokenizer = Tokenizer(test_input)
tokens = tokenizer.read_Tokens()
parser = Parser(tokens)
program = parser.program().result

codeGen = CodeGenerator(program)
codeGen.code_gen()