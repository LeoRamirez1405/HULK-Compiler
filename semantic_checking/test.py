import sys
import os
current_dir = os.getcwd()
sys.path.insert(0, current_dir)

from AST import *
from semantic_checking.semantic_checking import SemanticCheckingVisitor

ast = ProgramNode([PrintStatmentNode(NumberNode(4))])
checker = SemanticCheckingVisitor()
checker.visit(ast)