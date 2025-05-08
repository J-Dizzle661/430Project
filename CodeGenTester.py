import unittest
from Tokenizer import Tokenizer
from Parser import Parser
from CodeGenerator import *


test_input ='''
            class Animal{
                init(Int price,Int age){super(); }
            }

            class Dog extends Animal{
                Int age;
                Boolean isAlive;
                Int price;

                init(Int age, Boolean isAlive, Int price){super(isAlive, age, price); }

                method bark(Int age, Boolean isAlive) Void{
                    5 * 5;
                    2 * 7;
                    7 + 9;
                    false;
                    true;
                    10;
                    Int x;
                    Bool y = false;
                    Int z = 6 + 6;
                }
            }

            Int i = 0;
            Boolean j = true;
            Int k = 0 + i;

            '''

tokenizer = Tokenizer(test_input)
tokens = tokenizer.read_Tokens()
parser = Parser(tokens)
program = parser.program().result

codeGen = CodeGenerator(program)
codeGen.code_gen()