from tokens import *
from model import *
from utils import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0
   
    def advance(self):
        token = self.tokens[self.curr]
        self.curr = self.curr + 1
        return token

    def peek(self):
        return self.tokens[self.curr]

    def is_next(self, expected_type):
        if self.curr  >= len(self.tokens):
            return False
        return self.peek().token_type == expected_type

    def expect(self, expected_type):
        if self.curr  >= len(self.tokens):
            parse_error(f'Found {self.previous_token().lexeme!r} at the end of parsing', self.previous_token().line)
        elif self.peek().token_type == expected_type:
            token = self.advance()
            return token
        else:
            parse_error(f'Expected {expected_type}, found {self.peek().lexeme!r}.', self.peek().line)

    def previous_token(self):
        return self.tokens[self.curr - 1]

    def match(self, expected_type):
        if self.curr >= len(self.tokens):
            return False
        if self.peek().token_type != expected_type:
            return False
        self.curr = self.curr + 1
        return True

    # <primary> ::= <integer> | <float> | <bool> | <string> | '(' <expr> ')'
    def primary(self):
        if self.match(TOK_INTEGER):
            return Integer(int(self.previous_token().lexeme), line = self.previous_token().line)
        elif self.match(TOK_FLOAT):
            return Float(float(self.previous_token().lexeme), line = self.previous_token().line)
        elif self.match(TOK_TRUE):
            return Bool(True, line = self.previous_token().line)
        elif self.match(TOK_FALSE):
            return Bool(False, line = self.previous_token().line)
        elif self.match(TOK_STRING):
            return String(str(self.previous_token().lexeme[1:-1]), line = self.previous_token().line)
        elif self.match(TOK_LPAREN):
            expr = self.expr()
            if (not self.match(TOK_RPAREN)):
                parse_error(f'Error: ")" expected.', self.previous_token().line)
            else:
                return Grouping(expr, line = self.previous_token().line)
        else:
            identifier = self.expect(TOK_IDENTIFIER)
            if self.match(TOK_LPAREN):
                args = self.args()
                self.expect(TOK_RPAREN)
                return FuncCall(identifier.lexeme, args, line = self.previous_token().line)
            else:
                return Identifier(identifier.lexeme, line = self.previous_token().line)

    # <exponent> ::= <primary> ( '^' <exponent> )*
    def exponent(self):
        expr = self.primary()
        while self.match(TOK_CARET):
            op = self.previous_token()
            right = self.exponent()
            expr = BinOp(op, expr, right, line = op.line)
        return expr

    # <unary> ::= ( '+' | '-' | '~' )* <exponent>
    def unary(self):
        if self.match(TOK_PLUS) or self.match(TOK_MINUS) or self.match(TOK_NOT):
            op = self.previous_token()
            operand = self.unary()
            return UnOp(op, operand, line = op.line)
        return self.exponent()

    # <modulo> ::= <unary> ( "%" <unary> )*
    def modulo(self):
        expr = self.unary()
        if self.match(TOK_MOD):
            op = self.previous_token()
            right = self.unary()
            expr = BinOp(op, expr, right, line = op.line)
        return expr


    # <multiplication> ::= <unary> ( ('*'|'/') <unary> )*
    def multiplication(self):
        expr = self.modulo()
        while self.match(TOK_STAR) or self.match(TOK_SLASH):
            op = self.previous_token()
            right = self.modulo()
            expr = BinOp(op, expr, right, line = op.line)
        return expr

    # <addition> ::= <multiplication> ( ('+'|'-') <multiplication> )*
    def addition(self):
        expr = self.multiplication()
        while self.match(TOK_PLUS) or self.match(TOK_MINUS):
            op = self.previous_token()
            right = self.multiplication()
            expr = BinOp(op, expr, right, line = op.line)
        return expr

    # <comparison> ::= <addition> ( ( ">" | ">=" | "<" | "<=" ) <addition> ) *
    def comparison(self):
        expr = self.addition()
        while self.match(TOK_GT) or self.match(TOK_GE) or self.match(TOK_LT) or self.match(TOK_LE):
            op = self.previous_token()
            right = self.addition()
            expr = BinOp(op, expr, right, line = op.line)
        return expr

    # <equality> ::= <comparison> ( ( "~=" | "==" ) <comparison> )*
    def equality(self):
        expr = self.comparison()
        while self.match(TOK_NE) or self.match(TOK_EQEQ):
            op = self.previous_token()
            right = self.comparison()
            expr = BinOp(op, expr, right, line = op.line)
        return expr

    # <logical_and> ::= <equality> ( "and" <equality> )*
    def logical_and(self):
        expr = self.equality()
        while self.match(TOK_AND):
            op = self.previous_token()
            right = self.equality()
            expr = LogicalOp(op, expr, right, line = op.line)
        return expr

    # <logical_or> ::= <logical_and> ( "or" <logical_and> )*
    def logical_or(self):
        expr = self.logical_and()
        while self.match(TOK_OR):
            op = self.previous_token()
            right = self.logical_and()
            expr = LogicalOp(op, expr, right, line = op.line)
        return expr

    def expr(self):
        return self.logical_or()

    # <print_stmt> ::= "print" <expr>
    def print_stmt(self, end):
        if self.match(TOK_PRINT) or self.match(TOK_PRINTLN):
            val = self.expr()
            return PrintStmt(val, end, line = self.previous_token().line)

    # <if_stmt> ::= "if" <expr> "then" <stmts> ( "else" <stmts> )? "end"
    def if_stmt(self):
        self.expect(TOK_IF)
        test = self.expr()
        self.expect(TOK_THEN)
        then_stmts = self.stmts()
        if self.is_next(TOK_ELSE):
            self.advance() # Consume the else
            else_stmts = self.stmts()
        else:
            else_stmts = None
        self.expect(TOK_END)
        return IfStmt(test, then_stmts, else_stmts, line = self.previous_token().line)

    # <while_stmt> ::= "while" <expr> "do" <stmts> "end"
    def while_stmt(self):
        self.expect(TOK_WHILE)
        test = self.expr()
        self.expect(TOK_DO)
        stmts = self.stmts()
        self.expect(TOK_END)
        return WhileStmt(test, stmts, line = self.previous_token().line)

    # <for_stmt> ::= "for" <identifier> ":=" <start> "," <end> ("," <increment>)? "do" <stmts> "end"
    def for_stmt(self):
        self.expect(TOK_FOR)
        identifier = self.primary()
        self.expect(TOK_ASSIGN)
        start = self.expr()
        self.expect(TOK_COMMA)
        end = self.expr()
        step = None
        if self.is_next(TOK_COMMA):
            self.advance()
            step = self.expr()
        self.expect(TOK_DO)
        stmts = self.stmts()
        self.expect(TOK_END)
        return ForStmt(identifier, start, end, step, stmts, line = self.previous_token().line)

    # <params> ::= <identifier> ( "," <identifier> )*
    def params(self):
        params = []
        num = 0
        while not self.is_next(TOK_RPAREN):
            name = self.expect(TOK_IDENTIFIER)
            num += 1
            if num > 255:
                parse_error(f'Functions cannot have more than 255 parameters.', name.line)
            params.append(Param(name.lexeme, line = self.previous_token().line))
            if not self.is_next(TOK_RPAREN):
                self.expect(TOK_COMMA)
        return params

    # <args> ::= <expr> ( "," <expr> )*
    def args(self):
        args = []
        while not self.is_next(TOK_RPAREN):
            args.append(self.expr())
            if not self.is_next(TOK_RPAREN):
                self.expect(TOK_COMMA)
        return args

    # <func_decl> ::= "func" <name> "(" <params>? ")" <stmts> "end"
    def func_decl(self):
        self.expect(TOK_FUNC)
        name = self.expect(TOK_IDENTIFIER)
        self.expect(TOK_LPAREN)
        params = self.params()
        self.expect(TOK_RPAREN)
        stmts = self.stmts()
        self.expect(TOK_END)
        return FuncDecl(name.lexeme, params, stmts, line = self.previous_token().line)

    # <local_assign> ::= "local" <assign>
    def local_assign(self):
        self.expect(TOK_LOCAL)
        left = self.expr()
        self.expect(TOK_ASSIGN)
        right = self.expr()
        return LocalAssignment(left, right, line = self.previous_token().line)

    # <ret_stmt> ::= "ret" <expr>
    def ret_stmt(self):
        self.expect(TOK_RET)
        value = self.expr()
        return RetStmt(value, line = self.previous_token().line)

    # Predicitve parsing. The next token predicts the next statement.
    # <stmt> ::= print_stmt  | if_stmt | assign | local_assign | while_stmt | for_stmt | func_decl | func_call | ret_stmt
    def stmt(self):
        if self.peek().token_type == TOK_PRINT:
            return self.print_stmt(end='')
        elif self.peek().token_type == TOK_PRINTLN:
            return self.print_stmt(end='\n')
        elif self.peek().token_type == TOK_IF:
            return self.if_stmt()
        elif self.peek().token_type == TOK_WHILE:
            return self.while_stmt()
        elif self.peek().token_type == TOK_FOR:
            return self.for_stmt()
        elif self.peek().token_type == TOK_FUNC:
            return self.func_decl()
        elif self.peek().token_type == TOK_RET:
            return self.ret_stmt()
        elif self.peek().token_type == TOK_LOCAL:
            return self.local_assign()
        else:
            left = self.expr()
            # Asssignment:
            if self.match(TOK_ASSIGN):
                right = self.expr()
                return Assignment(left, right, line = self.previous_token().line)
            # Function call statement (special type of statement wrapping a FuncCall expression)
            else:
                return FuncCallStmt(left)

    def stmts(self):
        stmts = []
        # Loop all statements of the current block (until an "end", "else" or EOF is found)
        while self.curr < len(self.tokens) and not self.is_next(TOK_ELSE) and not self.is_next(TOK_END):
            stmt = self.stmt()
            stmts.append(stmt)
        return Stmts(stmts, line = self.previous_token().line)

    # <program> ::= <stmt>*
    def program(self):
        stmts = self.stmts()
        return stmts

    def parse(self):
        ast = self.program()
        return ast

