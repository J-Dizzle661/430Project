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
                Int age;
                init(Int age) {this.age = age; }
                method speak() Void { println("PC Noises"); }
                method getAge() Int { return this.age; }
                }
                class Cat extends Animal {
                init(Int age) { super(age); }
                method speak() Void { println("Meow"); }
                }
                class Dog extends Animal {
                init(Int age) { super(age); }
                method speak() Void { println("Bark"); }
                }

            
                Animal cat;
                Animal dog;
                cat = new Cat(5);
                dog = new Dog(6);
                cat.speak();
                dog.speak();
                int i = 0;

                if(i < 1){i = 5;}

                else {println("Failure");} 

                {Int j = 10; Boolean bool = false;}

                while (i > 0){i = i - 1;}
                println(i);
                println(cat.getAge());
                println(dog.getAge());
                '''
    main(input_code)
