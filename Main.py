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
return this.age;
                '''
    main(input_code)
