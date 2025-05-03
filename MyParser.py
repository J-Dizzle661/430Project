from Tokenizer import Tokenizer, Id_Token, IntLiteral_Token
from ReserveWords import *
from Symbols import *
from Operations import *
from AST import Node
from Productions import *
from Expressions import Exp, IdExp, CallExp, IntLiteral, BooleanLiteral
from dataclasses import dataclass

@dataclass
class ParseResult:
    result: any
    next_pos: int

class ParseException(Exception):
    def __init__(self, message):
        super().__init__(message)

class MyParser:
    def __init__(self, tokens):
       self.tokens = tokens
       self.position = 0

    def read_token(self, x):
        if (x < 0 or x >= len(self.tokens)):
            raise Exception(f"Ran out of tokens")
        else:
            return self.tokens[x]
        
    def assert_token_is(self, pos, expected_token):
        actual_token = self.read_token(pos)
        if not isinstance(actual_token, type(expected_token)):
            raise ParseException(
                f"Expected token {type(expected_token).__name__} at position {pos}, "
                f"but found {type(actual_token).__name__}"
        )

    def program(self):
        pos = self.position
        stmts = []
        classes = []

        while pos < len(self.tokens):
            token = self.read_token(pos)

            # Try to parse a class definition
            if isinstance(token, class_token):
                class_result = self.classdef(pos + 1)
                classes.append(class_result.result)
                pos = class_result.next_pos

            # Try to parse a statement
            else:
                try:
                    stmt_result = self.stmt(pos)
                    stmts.append(stmt_result.result)
                    pos = stmt_result.next_pos
                except ParseException as e:
                    raise ParseException(f"Failed to parse at position {pos}: {e}")


        return ParseResult(Program(classes, stmts), pos)
    

    def classdef(self, pos):
        # 'class'
        # token = self.read_token(pos)
        # if token.value != "class":    #this is not needed because the class instance is already checked in line 39*
        #     raise ParseException(f"Expected 'class' at position {pos}")
        # pos += 1

        # classname
        token = self.read_token(pos)
        if not isinstance(token, Id_Token):
            raise ParseException(f"Expected class name at position {pos}")
        class_name = token.value
        pos += 1

        # optional 'extends'
        token = self.read_token(pos)
        extends_name = None
        if not isinstance(token, Extends_token):
            pos += 1
            token = self.read_token(pos)
            if not isinstance(token, Id_Token):
                raise ParseException(f"Expected superclass name at position {pos}")
            extends_name = token.value
            pos += 1

        # '{'
        #self.assert_token_is(pos, LSBracket_Token())

        if not isinstance(self.read_token(pos), LSBracket_Token):
           raise ParseException(f"Expected Leftbracket at position {pos}") 
        pos += 1

        # # parse vardec*     #
        # vardecs = []
        # while isinstance(self.read_token(pos), (Int_Type, Boolean_Type, Void_Type)):
        #     vardec_result = self.vardec_parser(pos)
        #     vardecs.append(vardec_result.result)
        #     pos = vardec_result.next_pos
        #     self.assert_token_is(pos, SemiColon_Token())
        #     pos += 1

        # were gonna parse stmts next even though the grammar doesnt explicitly state  

        # parse constructor (optional)
        # constructors = []  # our language can only have one constructor per class 
        if isinstance(self.read_token(pos), init_token):
            # constructor_result = self.constructor(pos + 1) #methoddef and constructordef are basically the same
            constructor_result = self.methoddef(pos + 1, 'init')
            pos = constructor_result.next_pos

        # parse methoddef*
        methods = []
        while self.read_token(pos).value == "method":
            method_result = self.constructor_or_method(pos)
            methods.append(method_result.result)
            pos = method_result.next_pos

        # '}'
        self.assert_token_is(pos, RSBracket_Token())
        pos += 1

        return ParseResult(Class_Def(class_name, vardecs, constructors + methods, extends_name), pos)

    def methoddef(self, pos):

        if (not isinstance (self.pos, Id_Token)):
            raise ParseException(f"Expected ID token at position {pos}")
        name = self.tokens[pos].value
        pos += 1 

        if not isinstance (self.pos, LP_Token):
            raise ParseException(f"Expected LP token at position {pos}")
        pos += 1

        commaVardec = self.comma_vardec_parser(pos)
        params = params_result.result
        pos = commaVardec.next_pos + 1

        self.assert_token_is(pos, RP_Token())
        pos += 1

        type_result = self.type_parser(pos)
        return_type = type_result.result
        pos = type_result.next_pos

        if not isinstance(self.tokens[pos], LBracket_Token):
            raise ParseException(f"Expected LBracket token at position {pos}")
        pos += 1

        stmts = []
        while not isinstance(self.read_token(pos), RSBracket_Token):
            stmt_result = self.stmt(pos)
            stmts.append(stmt_result.result)
            pos = stmt_result.next_pos

        self.assert_token_is(pos, RSBracket_Token())  # Adjusted to match RSBracket_Token
        pos += 1        
            
        method = MethodDef()




    
    
    
    #####
    def comma_vardec_parser(self, pos):
        vardecs = []

        if isinstance(self.read_token(pos), RP_Token):
            return ParseResult(vardecs, pos)
    
        vd = self.vardec_parser(pos)
        vardecs.append(vd.result)
        pos = vd.next_pos

        while pos < len(self.tokens):
            token = self.read_token(pos)
            if not isinstance(token, Comma_Token):
                break
            pos += 1
            vd = self.vardec_parser(pos)
            vardecs.append(vd.result)
            pos = vd.next_pos

        return ParseResult(vardecs, pos)



