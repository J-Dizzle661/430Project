from Tokenizer import *
import unittest

class TestTokenizer(unittest.TestCase):
    def test_reserve_words_types(self):
        types = Tokenizer('Int Boolean Void')
        types.read_Tokens()
        self.assertEqual(['Int_token(Int)', 'Boolean_token(Boolean)', 'Void_token(Void)'], types.get_tokens_as_str())

    def test_reserve_words_expressions(self):
        expressions = Tokenizer('this true false println new')
        expressions.read_Tokens()
        self.assertEqual(['this_token(this)', 'true_token(true)', 'false_token(false)', 'print_token(println)', 'new_token(new)'], 
                         expressions.get_tokens_as_str())
        
    def test_reserve_words_stmts(self):
        stmts = Tokenizer('while break return if else')
        stmts.read_Tokens()
        self.assertEqual(['while_token(while)', 'break_token(break)', 'return_token(return)', 'if_token(if)', 'else_token(else)'],
                         stmts.get_tokens_as_str())
        
    def test_reserve_words_constructs(self):
        constructs = Tokenizer('method init super class extends')
        constructs.read_Tokens()    
        self.assertEqual(['method_token(method)', 'init_token(init)', 'super_token(super)', 'this_token(this)', 'Id_Token(extends)'],
                         constructs.get_tokens_as_str())
    
    def test_symbols_one(self):
        first_half_symbols = Tokenizer('( ) [ ] { } ; ,')
        first_half_symbols.read_Tokens()
        self.assertEqual(['LP_Token(()', 'RP_Token())', 'LBracket_Token(])', 'RBracket_Token([)', 'RSBracket_Token({)',
                          'LSBracket_Token(})', 'SemiColon_Token(;)', 'Comma_Token(,)'], first_half_symbols.get_tokens_as_str())

    def test_symbols_two(self):
        second_half_symbols = Tokenizer(': => * / + - = .')
        second_half_symbols.read_Tokens()
        self.assertEqual(['Colon_Token(:)', 'Arrow_Token(=>)', 'Star_Token(*)', 'Div_Token(/)', 'Plus_Token(+)',
                         'Minus_Token(-)', 'Equals_Token(=)', 'Dot_Token(.)'], second_half_symbols.get_tokens_as_str())
        
    def test_ID_tokens(self):
        dummy_IDs = Tokenizer('foo bar baz')
        dummy_IDs.read_Tokens()
        self.assertEqual(['Id_Token(foo)', 'Id_Token(bar)', 'Id_Token(baz)'], dummy_IDs.get_tokens_as_str())

    def test_int_tokens(self):
        dummy_ints = Tokenizer('34 6 2')
        dummy_ints.read_Tokens()
        self.assertEqual(['Number_Token(34)', 'Number_Token(6)', 'Number_Token(2)'], dummy_ints.get_tokens_as_str())

    
if __name__ == '__main__':
    unittest.main()
    
def test_tokenizer():
    testinput = "34 6 2 5"
    tokenizer = Tokenizer(testinput)
    tokenizer.read_Tokens()
    print(tokenizer.get_tokens_as_str()) 

test_tokenizer()


''' 
    try:
        tokens = []
        while tokenizer.get_position() < len(testinput):
            token = tokenizer.read_Token()
            tokens.append(str(token))
        
        print("Tokens:", tokens)
    
    except Exception as e:
        print("Error message:", e)'
    '''    