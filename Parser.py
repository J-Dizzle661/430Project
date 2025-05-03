from Tokenizer import Tokenizer, Id_Token, IntLiteral_Token
from ReserveWords import *
from Symbols import *
from Operations import *
from AST import Node
from Productions import *
from Expressions import Exp, IdExp, CallExp, IntLiteral, BooleanLiteral
from dataclasses import dataclass

@dataclass
class LessThanOp:
    pass

@dataclass
class GreaterThanOp:
    pass

@dataclass
class Class_Type:
    name: str

@dataclass
class ParseResult:
    result: any
    next_pos: int

class ParseException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Parser():
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
    
    def type_parser(self, pos):
        tokens = self.tokens
        if pos >= len(tokens):
            raise ParseException("Expected type but ran out of tokens")
        token = tokens[pos]
        if isinstance(token, Int_token):  # ← Token from Tokenizer
            return ParseResult(Int_Type(), pos + 1)
        elif isinstance(token, Boolean_token):
            return ParseResult(Boolean_Type(), pos + 1)
        elif isinstance(token, Void_token):
            return ParseResult(Void_Type(), pos + 1)
        elif isinstance(token, Id_Token):  # Handle class names as types
            return ParseResult(Class_Type(token.value), pos + 1)
        else:
            raise ParseException(f"Expected type at position {pos}, but got: {token}")

    #comma_exp
    def comma_exp(self, start_pos):
        args = []

        if isinstance(self.read_token(start_pos), RP_Token):
            return ParseResult(args, start_pos)
    
        first = self.exp(start_pos)
        args.append(first.result)
        pos = first.next_pos

        while pos < len(self.tokens) and isinstance(self.read_token(pos), Comma_Token):
            pos += 1
            next_arg = self.exp(pos)
            args.append(next_arg.result)
            pos = next_arg.next_pos

        return ParseResult(args, pos)
    
    def primary_exp(self, start_pos):
        token = self.read_token(start_pos)
        #var
        if isinstance(token, Id_Token):
            return ParseResult(IdExp(token.value), start_pos + 1)
        #int
        elif isinstance(token, IntLiteral_Token):
            return ParseResult(IntLiteral(token.value), start_pos + 1)
        #this
        elif isinstance(token, this_token):
            return ParseResult(IdExp(token.value), start_pos + 1)
        #true
        elif isinstance(token, true_token):
            return ParseResult(BooleanLiteral(token.value), start_pos + 1)
        #false
        elif isinstance(token, false_token):
            return ParseResult(BooleanLiteral(token.value), start_pos + 1)
        #println
        elif isinstance(token, print_token):
            return ParseResult(IdExp(token.value), start_pos + 1)
        #new
        elif isinstance(token, new_token):
            pos = start_pos + 1
            class_token = self.read_token(pos)
            if not isinstance(class_token, Id_Token):
                raise ParseException(f"Expected class name after 'new' at position {pos}")
            pos += 1
            self.assert_token_is(pos, LP_Token())
            pos += 1
            args_result = self.comma_exp(pos)
            args = args_result.result
            pos = args_result.next_pos
            self.assert_token_is(pos, RP_Token())
            pos += 1
            return ParseResult(CallExp(IdExp("new"), [IdExp(class_token.value)] + args), pos)
        elif isinstance(token, LP_Token):
            e = self.exp(start_pos + 1)
            self.assert_token_is(e.next_pos, RP_Token())
            return ParseResult(e.result, e.next_pos + 1) 
        else:
            raise ParseException(f"Expected primary expression at position: {start_pos}")
        
    #create call_exp
    #call_exp has to call primary_exp
    def call_exp(self, start_pos):
        m = self.primary_exp(start_pos)
        result = m.result
        pos = m.next_pos
        while True:
            try:
                t = self.read_token(pos)
                if isinstance(t, Dot_Token):
                    pos += 1
                    field_token = self.read_token(pos)
                    if not isinstance(field_token, Id_Token):
                        raise ParseException(f"Expected field or method name after '.' at position {pos}")
                    pos += 1
                    if isinstance(self.read_token(pos), LP_Token):
                        pos += 1
                        args = []
                        if isinstance(self.read_token(pos), RP_Token):
                            pos += 1
                            result = CallExp(result, [IdExp(field_token.value)])
                            continue
                        args_parse = self.comma_exp(pos)
                        args = args_parse.result
                        pos = args_parse.next_pos
                        self.assert_token_is(pos, RP_Token())
                        pos += 1
                        result = CallExp(result, [IdExp(field_token.value)] + args)
                    else:
                        result = CallExp(result, [IdExp(field_token.value)])
                elif isinstance(t, LP_Token):
                    pos += 1
                    args = []
                    if isinstance(self.read_token(pos), RP_Token):
                        pos += 1
                        result = CallExp(result, [])
                        continue
                    args_parse = self.comma_exp(pos)
                    args = args_parse.result
                    pos = args_parse.next_pos
                    self.assert_token_is(pos, RP_Token())
                    pos += 1
                    result = CallExp(result, args)
                else:
                    break
            except ParseException:
                break
        return ParseResult(result, pos)

    def mult_exp(self, start_pos):
        m = self.call_exp(start_pos)
        result = m.result
        should_run = True
        pos = m.next_pos
        while should_run:
            try:
                t= self.read_token(pos)
                if isinstance(t, Star_Token):
                    op = MultOp()
                elif isinstance(t, Div_Token):
                    op = DivOp()
                else: 
                    raise ParseException("Expected * or /")
                m2 = self.call_exp(pos + 1)
                result = BinOpExp(result, op, m2.result)
                pos = m2.next_pos
            except ParseException:
                should_run = False
        return ParseResult(result, pos) #instead of returning parse result it should just call make_node function instead (that will build the tree)

    def add_exp(self, start_pos):
        m = self.mult_exp(start_pos)
        result = m.result
        pos = m.next_pos
        while True:
            try: 
                t = self.read_token(pos)
                if isinstance(t, Plus_Token):
                    op = PlusOp()
                elif isinstance(t, Minus_Token):
                    op = MinusOp()
                else: 
                    raise ParseException("Expected + or -")
                m2 = self.mult_exp(pos+1)
                result = BinOpExp(result, op, m2.result)
                pos = m2.next_pos
            except ParseException:
                break
        return ParseResult(result, pos)

    def comp_exp(self, start_pos):
        m = self.add_exp(start_pos)
        result = m.result
        pos = m.next_pos
        try:
            t = self.read_token(pos)
            if isinstance(t, Less_Than_Token):
                op = LessThanOp()
            elif isinstance(t, Greater_Than_Token):
                op = GreaterThanOp()
            else:
                return ParseResult(result, pos)
            m2 = self.add_exp(pos + 1)
            result = BinOpExp(result, op, m2.result)
            pos = m2.next_pos
        except ParseException:
            pass
        return ParseResult(result, pos)
    
    def exp(self, start_pos):
        return self.comp_exp(start_pos)
    
    def vardec_parser(self, pos):
        type_result = self.type_parser(pos)
        id_token = self.read_token(type_result.next_pos)

        if not isinstance(id_token, Id_Token):
            raise ParseException(f"Expected variable name at {type_result.next_pos}")

        var = Variable(id_token.value)
        return ParseResult(vardec_stmt(type_result.result, var), type_result.next_pos + 1)

    def stmt(self, start_pos):
        t = self.read_token(start_pos)

        # Try variable declaration (with or without initialization)
        try:
            type_result = self.type_parser(start_pos)
            id_token = self.read_token(type_result.next_pos)
            if isinstance(id_token, Id_Token):
                next_token = self.read_token(type_result.next_pos + 1)
                
                # Declaration with assignment
                if isinstance(next_token, Equals_Token):
                    e = self.exp(type_result.next_pos + 2)
                    self.assert_token_is(e.next_pos, SemiColon_Token())
                    return ParseResult(assign_stmt(Variable(id_token.value), e.result), e.next_pos + 1)

                # Simple declaration
                elif isinstance(next_token, SemiColon_Token):
                    return ParseResult(
                        vardec_stmt(type_result.result, Variable(id_token.value)),
                        type_result.next_pos + 2
                    )
        except ParseException:
            pass

        # while stmt
        if isinstance(t, while_token):
            self.assert_token_is(start_pos + 1, LP_Token())
            cond = self.exp(start_pos + 2)
            self.assert_token_is(cond.next_pos, RP_Token())
            self.assert_token_is(cond.next_pos + 1, LSBracket_Token())
            body = self.stmt(cond.next_pos + 1)  # This will parse the block
            return ParseResult(while_stmt(cond.result, body.result), body.next_pos)

        # break stmt 
        if isinstance(t, break_token):
            self.assert_token_is(start_pos + 1, SemiColon_Token())
            return ParseResult(break_stmt(), start_pos + 2)

        # return stmt
        if isinstance(t, return_token):
            next_token = self.read_token(start_pos + 1)
            if isinstance(next_token, SemiColon_Token):
                return ParseResult(return_stmt(Exp()), start_pos + 2)
            else:
                e = self.exp(start_pos + 1)
                self.assert_token_is(e.next_pos, SemiColon_Token())
                return ParseResult(return_stmt(e.result), e.next_pos + 1)

        # if else stmt
        if isinstance(t, if_token):
            self.assert_token_is(start_pos + 1, LP_Token())
            cond = self.exp(start_pos + 2)
            self.assert_token_is(cond.next_pos, RP_Token())
            then_stmt = self.stmt(cond.next_pos + 1)
            pos = then_stmt.next_pos
            try:
                if isinstance(self.read_token(pos), else_token):
                    else_stmt = self.stmt(pos + 1)
                    return ParseResult(if_stmt(cond.result, then_stmt.result, else_stmt.result), else_stmt.next_pos)
            except ParseException:
                pass
            return ParseResult(if_stmt(cond.result, then_stmt.result), pos)

        # stmt* (block)
        if isinstance(t, LSBracket_Token):
            pos = start_pos + 1
            stmts = []
            while not isinstance(self.read_token(pos), RSBracket_Token):
                try:
                    s = self.stmt(pos)
                    stmts.append(s.result)
                    pos = s.next_pos
                except ParseException as e:
                    raise
            return ParseResult(block_stmt(stmts), pos + 1)

        # assignment (including field assignments)
        if isinstance(t, (Id_Token, this_token)):
            pos = start_pos
            var = None
            
            # Handle field access (this.field)
            if isinstance(t, this_token):
                pos += 1
                self.assert_token_is(pos, Dot_Token())
                pos += 1
                field_token = self.read_token(pos)
                if not isinstance(field_token, Id_Token):
                    raise ParseException(f"Expected field name after 'this.' at position {pos}")
                var = Variable(field_token.value)
                pos += 1
            else:
                var = Variable(t.value)
                pos += 1

            # Check for equals
            if isinstance(self.read_token(pos), Equals_Token):
                pos += 1
                e = self.exp(pos)
                self.assert_token_is(e.next_pos, SemiColon_Token())
                return ParseResult(assign_stmt(var, e.result), e.next_pos + 1)

        # expression stmt (including method calls)
        try:
            # Try to parse a method call or field access
            if isinstance(t, Id_Token):
                next_token = self.read_token(start_pos + 1)
                if isinstance(next_token, (Dot_Token, LP_Token)):
                    call_result = self.call_exp(start_pos)
                    self.assert_token_is(call_result.next_pos, SemiColon_Token())
                    return ParseResult(exp_stmt(call_result.result), call_result.next_pos + 1)
            
            # Try to parse a regular expression
            e = self.exp(start_pos)
            next_token = self.read_token(e.next_pos)
            if isinstance(next_token, SemiColon_Token):
                return ParseResult(exp_stmt(e.result), e.next_pos + 1)
        except ParseException:
            pass

        # Try to parse a method call without checking token type first
        try:
            call_result = self.call_exp(start_pos)
            self.assert_token_is(call_result.next_pos, SemiColon_Token())
            return ParseResult(exp_stmt(call_result.result), call_result.next_pos + 1)
        except ParseException:
            pass

        raise ParseException(f"Invalid statement at position {start_pos}")

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
    
    def methoddef(self, start_pos):
        pos = start_pos

        token = self.read_token(pos)
        if not isinstance(token, method_token):
            raise ParseException(f"Expected 'method' at position {pos}")
        pos += 1

        token = self.read_token(pos)
        if not isinstance(token, Id_Token):
            raise ParseException(f"Expected method name at position {pos}")
        method_name = token.value
        pos += 1

        self.assert_token_is(pos, LP_Token())
        pos += 1

        params_result = self.comma_vardec_parser(pos)
        params = params_result.result
        pos = params_result.next_pos

        self.assert_token_is(pos, RP_Token())
        pos += 1

        type_result = self.type_parser(pos)
        return_type = type_result.result
        pos = type_result.next_pos

        self.assert_token_is(pos, LSBracket_Token())  # Adjusted to match LSBracket_Token
        pos += 1

        stmts = []
        while not isinstance(self.read_token(pos), RSBracket_Token):
            stmt_result = self.stmt(pos)
            stmts.append(stmt_result.result)
            pos = stmt_result.next_pos

        self.assert_token_is(pos, RSBracket_Token())  # Adjusted to match RSBracket_Token
        pos += 1

        method = MethodDef(method_name, params, return_type, stmts)
        return ParseResult(method, pos)
    
    def constructor(self, pos):
        # 'init' or 'constructor'
        token = self.read_token(pos)
        if token.value not in ["init", "constructor"]:
            raise ParseException(f"Expected 'init' or 'constructor' at position {pos}")
        pos += 1

        # '('
        self.assert_token_is(pos, LP_Token())
        pos += 1

        # comma_vardec
        params_result = self.comma_vardec_parser(pos)
        comma_vardec = params_result.result
        pos = params_result.next_pos

        # ')'
        self.assert_token_is(pos, RP_Token())
        pos += 1

        # '{'
        self.assert_token_is(pos, LSBracket_Token())
        pos += 1

        # 'super'
        self.assert_token_is(pos, super_token())
        pos += 1

        # '('
        self.assert_token_is(pos, LP_Token())
        pos += 1

        # comma_exp
        comma_exp_result = self.comma_exp(pos)
        super_args = comma_exp_result.result
        pos = comma_exp_result.next_pos

        # ')'
        self.assert_token_is(pos, RP_Token())
        pos += 1

        # ';'
        self.assert_token_is(pos, SemiColon_Token())
        pos += 1

        # parse stmt*
        stmts = []
        while not isinstance(self.read_token(pos), RSBracket_Token):
            stmt_result = self.stmt(pos)
            stmts.append(stmt_result.result)
            pos = stmt_result.next_pos

        # '}'
        self.assert_token_is(pos, RSBracket_Token())
        pos += 1

        constructor = constructor_method(comma_vardec, super_args, stmts)
        return ParseResult(constructor, pos)

    def classdef(self, pos):
        # 'class'
        token = self.read_token(pos)
        if token.value != "class":
            raise ParseException(f"Expected 'class' at position {pos}")
        pos += 1

        # classname
        token = self.read_token(pos)
        if not isinstance(token, Id_Token):
            raise ParseException(f"Expected class name at position {pos}")
        class_name = token.value
        pos += 1

        # optional 'extends'
        extends_name = None
        if pos < len(self.tokens) and self.read_token(pos).value == "extends":
            pos += 1
            token = self.read_token(pos)
            if not isinstance(token, Id_Token):
                raise ParseException(f"Expected superclass name at position {pos}")
            extends_name = token.value
            pos += 1

        # '{'
        if not isinstance(self.read_token(pos), LSBracket_Token):
            raise ParseException(f"Expected '{{' at position {pos}")
        pos += 1

        # parse vardec*
        vardecs = []
        while True:
            if pos >= len(self.tokens):
                raise ParseException(f"Unexpected end of tokens while parsing class {class_name}")
            token = self.read_token(pos)
            if not isinstance(token, (Int_token, Boolean_token, Void_token)):
                break
            vardec_result = self.vardec_parser(pos)
            vardecs.append(vardec_result.result)
            pos = vardec_result.next_pos
            self.assert_token_is(pos, SemiColon_Token())
            pos += 1

        # parse constructor (optional)
        constructors = []
        if pos < len(self.tokens) and self.read_token(pos).value in ["init", "constructor"]:
            constructor_result = self.constructor(pos)
            constructors.append(constructor_result.result)
            pos = constructor_result.next_pos

        # parse methoddef*
        methods = []
        while pos < len(self.tokens) and self.read_token(pos).value == "method":
            method_result = self.methoddef(pos)
            methods.append(method_result.result)
            pos = method_result.next_pos

        # '}'
        if pos >= len(self.tokens):
            raise ParseException(f"Unexpected end of tokens while parsing class {class_name}")
        if not isinstance(self.read_token(pos), RSBracket_Token):
            raise ParseException(f"Expected '}}' at position {pos}")
        pos += 1

        return ParseResult(Class_Def(class_name, vardecs, constructors, methods, extends_name), pos)

    def program(self, start_pos=0):
        pos = start_pos
        stmts = []
        classes = []

        while pos < len(self.tokens):
            token = self.read_token(pos)

            # Try to parse a class definition
            if token.value == "class":
                class_result = self.classdef(pos)
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
    
def traverse_exp(exp):
    match(exp):
        case BinOpExp():
            return Node(exp)
        case Int_Type():
            return Node
    
def traverse_stmt():
    pass

def build_exp_node(exp):
    node = Node(exp)

    if isinstance(exp, BinOpExp):
        node.add_child(build_exp_node(exp.left))
        node.add_child(Node(exp.op))
        node.add_child(build_exp_node(exp.right))

    elif isinstance(exp, IdExp):
        pass

    elif isinstance(exp, IntLiteral):
        pass

    elif isinstance(exp, BooleanLiteral):
        node.add_child(Node(exp.value))

    elif isinstance(exp, CallExp):
        node.add_child(build_exp_node(exp.func))
        for arg in exp.args:
            node.add_child(build_exp_node(arg))

    return node

def makeTree(program):
    #do something that takes in a production
    #and spits out a node, which is then added to the AST
    tree = Node(program) 

    for stmt in program.stmts:
        stmt_node = Node(stmt)
        tree.add_child(stmt_node)

        # Add children based on statement type
        if isinstance(stmt, assign_stmt):
            stmt_node.add_child(Node(stmt.variable))
            stmt_node.add_child(build_exp_node(stmt.exp))

        elif isinstance(stmt, vardec_stmt):
            stmt_node.add_child(Node(stmt.type))
            stmt_node.add_child(Node(stmt.variable))

        elif isinstance(stmt, exp_stmt):
            stmt_node.add_child(build_exp_node(stmt.exp))


    for cls in program.classes:
        class_node = Node(cls)
        tree.add_child(class_node)

        for vardec in cls.vardecs:
            vardec_node = Node(vardec)
            class_node.add_child(vardec_node)
            vardec_node.add_child(Node(vardec.type))
            vardec_node.add_child(Node(vardec.variable))

        for method in cls.methods:
            method_node = Node(method)
            class_node.add_child(method_node)

            if hasattr(method, "comma_exp"):  # constructor_method
                super_call = CallExp(IdExp("super"), method.comma_exp)
                method_node.add_child(build_exp_node(super_call))

            for stmt in getattr(method, 'stmts', []):
                stmt_node = Node(stmt)
                method_node.add_child(stmt_node)

                if isinstance(stmt, return_stmt):
                    stmt_node.add_child(build_exp_node(stmt.exp))

                elif isinstance(stmt, exp_stmt):
                    stmt_node.add_child(build_exp_node(stmt.exp))

    return tree
