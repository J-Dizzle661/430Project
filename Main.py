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
    input_code = '''
                class Animal {
                    init() { }
                    method speak() Void { println("PC Noises!!!!"); }
                    }
                    class Cat extends Animal {
                    init() { super(); }
                    method speak() Void { println("Meow"); }
                    }
                    class Dog extends Animal {
                    init() { super(); }
                    method speak() Void { println("Bark"); }
                    }

                    Animal cat;
                    Animal dog;
                    cat = new Cat();
                    dog = new Dog();
                    cat.speak();
                    dog.speak();
                    int i = 0;

                    if(i < 1){i = 5;}

                    else {println("Failure");} 

                    while (i > 0){i = i - 1;}
                    println(i);
                '''
    main(input_code)
