import unittest
from Tokenizer import Tokenizer
from Parser import Parser
from CodeGenerator import *


test_input ='''
            class Animal{
                Int x;
                Boolean bool;
                Int y;
                init(){super();}
            }
            '''

tokenizer = Tokenizer(test_input)
tokens = tokenizer.read_Tokens()
parser = Parser(tokens)
program = parser.program().result

codeGen = CodeGenerator(program)
codeGen.code_gen()