import unittest
from Tokenizer import Tokenizer
from Parser import Parser
from CodeGenerator import *
import subprocess

input_code = '''
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
class TestCodeGen(unittest.TestCase):
    tokenizer = Tokenizer(input_code)
    parser = Parser(tokenizer.read_Tokens())
    code_gen = CodeGenerator((parser.program().result))
    code_gen.code_gen()

    def testCodeRun(self): # produces JS_Code.js file and runs in NodeJS, then console output is stores in js_output
        js_output = subprocess.run(['node', 'JS_Code.js'], capture_output= True, text = True)
        expected_output = 'Meow\nBark\n0\n5\n6\n'
        self.assertEqual(expected_output, js_output.stdout)

if __name__ == '__main__':
    unittest.main()