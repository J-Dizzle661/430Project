from Tokenizer import Tokenizer
from Parser import Parser
from CodeGenerator import CodeGenerator
import subprocess

def main(input_code):
    tokenizer = Tokenizer(input_code)
    parser = Parser(tokenizer.read_Tokens())
    code_gen = CodeGenerator((parser.program().result))
    code_gen.code_gen()

if __name__ == "__main__":
    input_code ='''
                class Animal {
                    init() {}
                    method speak() Void { println(0); }
                    }
                    class Cat extends Animal {
                    init() { super(); }
                    method speak() Void { println(1); }
                    }
                    class Dog extends Animal {
                    init() { super(); }
                    method speak() Void { println(2); }
                }
                Animal cat;
                Animal dog;
                cat = new Cat();
                dog = new Dog();
                cat.speak();
                dog.speak();
                '''
    main(input_code)
