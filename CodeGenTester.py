import unittest
from Tokenizer import Tokenizer
from Parser import Parser
from CodeGenerator import *


test_input ='''
            class Dog extends Animal{
                Int age;
                Boolean isAlive;
                Int price;
                init(int age, Boolean isAlive, Int price){super(age, isAlive, price);}
            }
            '''

tokenizer = Tokenizer(test_input)
tokens = tokenizer.read_Tokens()
parser = Parser(tokens)
program = parser.program().result

codeGen = CodeGenerator(program)
codeGen.code_gen()