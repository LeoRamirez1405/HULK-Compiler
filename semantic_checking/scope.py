from cmp.semantic import *

class Scope:
    def __init__(self, parent=None):
        self.local_variables = set()
        self.functions = {} # {key: id, valor: len(parameters)}
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)
        self.errors = []

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.local_variables.append(info)
        return info

    def find_variable(self, vname, index=None):
        locals = self.local_variables if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is None else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.local_variables if x.name == vname)
