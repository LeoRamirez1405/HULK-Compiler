from cmp.semantic import *

# class SemanticError(Exception):
#     @property
#     def text(self):
#         return self.args[0]

# class VariableInfo:
#     def __init__(self, name, vtype):
#         self.name = name
#         self.type = vtype
        
# class Type:
#     def __init__(self, name:str):
#         self.name = name
#         self.attributes = []
#         self.methods = []
#         self.parent = None

#     def set_parent(self, parent):
#         if self.parent is not None:
#             raise SemanticError(f'Parent type is already set for {self.name}.')
#         self.parent = parent

#     def get_attribute(self, name:str):
#         try:
#             return next(attr for attr in self.attributes if attr.name == name)
#         except StopIteration:
#             if self.parent is None:
#                 raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
#             try:
#                 return self.parent.get_attribute(name)
#             except SemanticError:
#                 raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

#     def define_attribute(self, name:str, typex):
#         try:
#             self.get_attribute(name)
#         except SemanticError:
#             attribute = Attribute(name, typex)
#             self.attributes.append(attribute)
#             return attribute
#         else:
#             raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

#     def get_method(self, name:str):
#         try:
#             return next(method for method in self.methods if method.name == name)
#         except StopIteration:
#             if self.parent is None:
#                 raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
#             try:
#                 return self.parent.get_method(name)
#             except SemanticError:
#                 raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

#     def define_method(self, name:str, param_names:list, param_types:list, return_type):
#         if name in (method.name for method in self.methods):
#             raise SemanticError(f'Method "{name}" already defined in {self.name}')

#         method = Method(name, param_names, param_types, return_type)
#         self.methods.append(method)
#         return method

#     def all_attributes(self, clean=True):
#         plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
#         for attr in self.attributes:
#             plain[attr.name] = (attr, self)
#         return plain.values() if clean else plain

#     def all_methods(self, clean=True):
#         plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
#         for method in self.methods:
#             plain[method.name] = (method, self)
#         return plain.values() if clean else plain

#     def conforms_to(self, other):
#         return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

#     def bypass(self):
#         return False

#     def __str__(self):
#         output = f'type {self.name}'
#         parent = '' if self.parent is None else f' : {self.parent.name}'
#         output += parent
#         output += ' {'
#         output += '\n\t' if self.attributes or self.methods else ''
#         output += '\n\t'.join(str(x) for x in self.attributes)
#         output += '\n\t' if self.attributes else ''
#         output += '\n\t'.join(str(x) for x in self.methods)
#         output += '\n' if self.methods else ''
#         output += '}\n'
#         return output

#     def __repr__(self):
#         return str(self)


class Scope:
    def __init__(self, parent=None):
        self.local_variables = set()
        self.functions = {} # {key: id, valor: len(parameters)}
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.local_variables.add(info)
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
    
class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name:str):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)