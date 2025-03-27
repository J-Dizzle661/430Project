from Tokenizer import Tokenizer

def test_tokenizer():
    testinput = "print ( )[ ]{ } ; , : => * / = + -"
    tokenizer = Tokenizer(testinput)

    try:
        tokens = []
        while tokenizer.get_position() < len(testinput):
            token = tokenizer.read_Token()
            tokens.append(str(token))
        
        print("Tokens:", tokens)
    
    except Exception as e:
        print("Error message:", e)

if __name__ == "__main__":
    test_tokenizer()