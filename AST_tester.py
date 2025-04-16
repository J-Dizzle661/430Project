import unittest
from Tokenizer import Tokenizer
from Parser import Parser, makeTree
from Productions import assign_stmt, vardec_stmt

class AST_tester(unittest.TestCase):
    def test_simple_declaration(self):
        tokenizer = Tokenizer('Int x;')
        tokens = tokenizer.read_Tokens()
        parser = Parser(tokens)
        stmt_result = parser.stmt(0)
        
        self.assertIsInstance(stmt_result.result, vardec_stmt)
        self.assertEqual(stmt_result.result.variable.var_name, 'x')

    def test_initialized_declaration(self):
        tokenizer = Tokenizer('Int x = 5;')
        tokens = tokenizer.read_Tokens()

        #print("TOKENS:", [type(tok).__name__ for tok in tokens])  # Debug print

        parser = Parser(tokens)

        try:
            stmt_result = parser.stmt(0)
            #print("ASSIGN TO:", stmt_result.result.variable.var_name)
            self.assertIsInstance(stmt_result.result, assign_stmt)
            self.assertEqual(stmt_result.result.variable.var_name, 'x')
        except Exception as e:
            self.fail(f"Parser threw an exception: {e}")
    
    def test_class_with_constructor_and_method(self):
        source = '''
            class Animal {
                constructor() super() {}
                method speak() Void { return println(0); }
            }
            '''
        tokenizer = Tokenizer(source)
        tokens = tokenizer.read_Tokens()
        parser = Parser(tokens)

        try:
            program = parser.program().result
            tree = makeTree(program)
            print("\nClass Tree:")
            print(tree.to_string())

            # Optional: basic assertions
            self.assertEqual(len(program.classes), 1)
            self.assertEqual(program.classes[0].class_name, "Animal")
            self.assertEqual(len(program.classes[0].methods), 2)  # constructor + method

        except Exception as e:
            self.fail(f"Parser threw an exception for class grammar: {e}")

    def test_full_program_ast_tree(self):
        source = '''
            class Animal {
                constructor() super() {}
                method speak() Void { return println(0); }
            }
            '''
        tokenizer = Tokenizer(source)
        tokens = tokenizer.read_Tokens()
        print("TOKENS:", [(type(tok).__name__, getattr(tok, 'value', '')) for tok in tokens])
        parser = Parser(tokens)
        program = parser.program().result
        
        tree = makeTree(program)
        print("\nFull Program AST:")
        print(tree.to_string())

if __name__ == '__main__':
    unittest.main()
