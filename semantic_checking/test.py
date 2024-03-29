import sys
import os
current_dir = os.getcwd()
sys.path.insert(0, current_dir)
# from semantic_checking.ast_nodes import *
from semantic_checking.semantic_checking import SemanticCheckingVisitor

a = 15

def test():
    a = 23
    print(a)
    
test()