from tokens import *

class Expr:
    '''
    Expressions evaluate to a result. Example: x + (2 * y) >= 6
    '''
    #TODO:
    pass

class Stmt:
    '''
    Statements perform an action. Example:
    '''
    #TODO:
    pass

class Integer(Expr):
    '''
    Example: 17
    '''
    def __init__(self, value):
        assert isinstance(value, int), value
        self.value = value
    def __repr__(self):
        return f'Integer[{self.value}]'

class Float(Expr):
    '''
    Example: 3.131592
    '''
    def __init__(self, value):
        assert isinstance(value, float), value
        self.value = value
    def __repr__(self):
        return f'Float[{self.value}]'

class UnOp(Expr):
    '''
    Example: -operand
    '''
    def __init__(self, op: Token, operand: Expr):
        assert isinstance(op, Token), op
        assert isinstance(operand, Expr), operand
        self.op = op
        self.operand = operand
    def __repr__(self):
        return f'UnOp({self.op.lexeme!r}, {self.operand})'

class Grouping(Expr):
    '''
    Example: ( <expr> )
    '''
    def __init__(self, value):
        assert isinstance(value, Expr), value
        self.value = value
    def __repr__(self):
        return f'Grouping({self.value})'

class BinOp(Expr):
    '''
    Example: x + y
    '''
    def __init__(self, op: Token, left: Expr, right: Expr):
        assert isinstance(op, Token), op
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.op = op
        self.left = left
        self.right = right
    def __repr__(self):
        return f'BinOp({self.op.lexeme!r}, {self.left}, {self.right})'

class WhileStmt(Stmt):
    #TODO:
    pass

class Assignment(Stmt):
    #TODO:
    pass

