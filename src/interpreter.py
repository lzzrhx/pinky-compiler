from model import *
from tokens import *
from utils import *
from state import *
import codecs

################################################################################
# Constants for different runtime value types
################################################################################
TYPE_NUMBER = 'TYPE_NUMBER' # 64-bit float
TYPE_STRING = 'TYPE_STRING' # String managed by the host language (Python)
TYPE_BOOL   = 'TYPE_BOOL'   # true or false

class Interpreter:
    def __init__(self):
        pass

    def interpret(self, node, env):
        if isinstance(node, Integer):
            return (TYPE_NUMBER, float(node.value))

        elif isinstance(node, Float):
            return (TYPE_NUMBER, float(node.value))
        
        elif isinstance(node, Bool):
            return (TYPE_BOOL, node.value)

        elif isinstance(node, String):
            return (TYPE_STRING, str(node.value))

        elif isinstance(node, Grouping):
            return (self.interpret(node.value, env))

        elif isinstance(node, Identifier):
            value = env.get_var(node.name)
            if value is None:
                runtime_error(f'Undeclared identifier {node.name!r}', node.line)
            if value[1] is None:
                runtime_error(f'Uninitialized identifier {node.name!r}', node.line)
            return value

        elif isinstance(node, Assignment):
            # Evaluate the righ-hand side expression
            righttype, rightval = self.interpret(node.right, env)
            # Update the value of the variable of create a new one
            env.set_var(node.left.name, (righttype, rightval))

        elif isinstance(node, BinOp):
            lefttype, leftval = self.interpret(node.left, env)
            righttype, rightval = self.interpret(node.right, env)
            
            if node.op.token_type == TOK_PLUS:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval + rightval)
                elif lefttype == TYPE_STRING or righttype == TYPE_STRING:
                    return (TYPE_STRING, stringify(leftval) + stringify(rightval))
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
            
            elif node.op.token_type == TOK_MINUS:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval - rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
            
            elif node.op.token_type == TOK_STAR:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval * rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
            
            elif node.op.token_type == TOK_SLASH:
                if rightval == 0:
                    runtime_error(f'Division by zero.', node.line)
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval / rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
            
            elif node.op.token_type == TOK_MOD:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval % rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
            
            elif node.op.token_type == TOK_CARET:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval ** rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
            
            elif node.op.token_type == TOK_GT:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING):
                    return (TYPE_BOOL, leftval > rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
            
            elif node.op.token_type == TOK_GE:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING):
                    return (TYPE_BOOL, leftval >= rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
            
            elif node.op.token_type == TOK_LT:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING):
                    return (TYPE_BOOL, leftval < rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
            
            elif node.op.token_type == TOK_LE:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING):
                    return (TYPE_BOOL, leftval <= rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
            
            elif node.op.token_type == TOK_EQEQ:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING) or (lefttype == TYPE_BOOL and righttype == TYPE_BOOL):
                    return (TYPE_BOOL, leftval == rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
            
            elif node.op.token_type == TOK_NE:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING) or (lefttype == TYPE_BOOL and righttype == TYPE_BOOL):
                    return (TYPE_BOOL, leftval != rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)
        
        elif isinstance(node, LogicalOp):
            lefttype, leftval = self.interpret(node.left, env)
            if node.op.token_type == TOK_OR:
                if leftval:
                    return (lefttype, leftval)
            elif node.op.token_type == TOK_AND:
                if not leftval:
                    return (lefttype, leftval)
            return self.interpret(node.right, env)

        elif isinstance(node, UnOp):
            operandtype, operandval = self.interpret(node.operand, env)
            
            if node.op.token_type == TOK_PLUS:
                if operandtype == TYPE_NUMBER:
                    return (TYPE_NUMBER, operandval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} with {operandtype}.', node.op.line)
            
            elif node.op.token_type == TOK_MINUS:
                if operandtype == TYPE_NUMBER:
                    return (TYPE_NUMBER, -operandval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} with {operandtype}.', node.op.line)
            
            elif node.op.token_type == TOK_NOT:
                if operandtype == TYPE_BOOL:
                    return (TYPE_BOOL, not operandval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} with {operandtype}.', node.op.line)

        elif isinstance(node, Stmts):
            for stmt in node.stmts:
                self.interpret(stmt, env)

        elif isinstance(node, PrintStmt):
            exprtype, exprval = self.interpret(node.value, env)
            print(codecs.escape_decode(bytes(stringify(exprval), "utf-8"))[0].decode("utf-8"), end = node.end)

        elif isinstance(node, IfStmt):
            testtype, testval = self.interpret(node.test, env)
            if testtype != TYPE_BOOL:
                runtime_error("Condition test is not a boolean expression.", node.line)
            if testval:
                self.interpret(node.then_stmts, env.new_env())
            else: 
                self.interpret(node.else_stmts, env.new_env())

        elif isinstance(node, WhileStmt):
            new_env = env.new_env()
            while True:
                testtype, testval = self.interpret(node.test, env)
                if testtype != TYPE_BOOL:
                    runtime_error("Condition test is not a boolean expression.", node.line)
                if not testval:
                    break
                self.interpret(node.stmts, new_env)

        elif isinstance(node, ForStmt):
            varname = node.ident.name
            itype, i = self.interpret(node.start, env)
            endtype, end = self.interpret(node.end, env)
            new_env = env.new_env()
            if i < end:
                step = 1
                if node.step is not None:
                    steptype, step = self.interpret(node.step, env)
                while i <= end:
                    newval = (TYPE_NUMBER, i)
                    env.set_var(varname, newval)
                    self.interpret(node.stmts, new_env)
                    i = i + step
            else:
                step = -1
                if node.step is not None:
                    steptype, step = self.interpret(node.step, env)
                while i >= end:
                    newval = (TYPE_NUMBER, i)
                    env.set_var(varname, newval)
                    self.interpret(node.stmts, new_env)
                    i = i + step

    # Interpreter entry point, creating a brand new global (parent) environment
    def interpret_ast(self, node):
        env = Environment()
        self.interpret(node, env)

