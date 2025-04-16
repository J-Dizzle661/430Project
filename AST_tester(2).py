from Tokenizer import Tokenizer
from Parser import Parser  # your actual parser class
import Productions  # your AST node classes

def test_case(input_code: str):
    print(f"\n=== Test: {input_code} ===")
    tokenizer = Tokenizer(input_code)
    tokens = tokenizer.read_Tokens()
    print("Tokens:", tokens)

    parser = Parser(tokens)  # Pass list of tokens, not the tokenizer itself
    tree = parser.program()  # Adjust this if your entry method is named differently
    print("AST Tree:")
    print(tree)

if __name__ == "__main__":
    test_case("Int x;")
    test_case("x = 5;")
    
