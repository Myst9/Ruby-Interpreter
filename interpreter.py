from parser_ruby import *

class Interpreter(NodeVisitor):
    
    GLOBAL_MEMORY = {}
    
    def __init__(self, tree):
        self.tree = tree

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == MOD:
            return self.visit(node.left) % self.visit(node.right)
        elif node.op.type == EQUAL:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == NOT:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.type == GRE:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == LESE:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == GRET:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == LEST:
            return self.visit(node.left) < self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        var_value = self.visit(node.right)
        self.GLOBAL_MEMORY[var_name] = var_value

    def visit_Var(self, node):
        var_name = node.value
        var_value = self.GLOBAL_MEMORY.get(var_name)
        if var_value is None:
            raise NameError(repr(var_name))
        return var_value

    def visit_If(self, node):
        if self.visit(node.condition):
            self.visit(node.body)
        else:
            self.visit(node.rest)

    def visit_Else(self, node):
        self.visit(node.body)

    def visit_While(self, node):
        while self.visit(node.condition):
            self.visit(node.body)

    def visit_list(self, node):
        for child in node:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)