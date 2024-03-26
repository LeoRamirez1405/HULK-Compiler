from ast_nodes import *
from .semantic_checking import SemanticCheckingVisitor

ast = ProgramNode([NumberNode(Token('5', int, (0,0)), 5)])
semantic_checker = SemanticCheckingVisitor()
semantic_checker.visit(ast)