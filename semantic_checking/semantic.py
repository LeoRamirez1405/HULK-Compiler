import itertools as itt
from collections import OrderedDict
from typing import List

class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]
    
class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type: Type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)
    
class Argument:
    def __init__(self, name, typex):
        self.name = name
        self.type: Type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, vname, vtype ): # ,value
        self.name = vname
        self.type = vtype
        # self.value = value
        
class Type:
    def __init__(self, name:str):
        self.name = name
        self.inhertance: Type = None
        self.args: List[Argument] = []
        self.attributes: List[Attribute] = []
        self.attrs_expression = {}
        self.methods: List[Method] = []
        self.parent = None

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            
    def get_arg(self, name:str):
        try:
            return next(arg for arg in self.args if arg.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Argument "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_arg(name)
            except SemanticError:
                raise SemanticError(f'Argument "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')
        
    def define_arg(self, name:str, typex):
        try:
            self.get_arg(name)
        except SemanticError:
            arg = Argument(name, typex)
            self.args.append(arg)
            return arg
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.inhertance is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.inhertance.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def set_attribute_expression(self, name:str, typex, expression):
        try:
            # attr = self.get_attribute(name)
            self.attrs_expression[name] = expression
        except SemanticError:
            pass
        #     attribute = Attribute(name, typex)
        #     self.attributes.append(attribute)
        #     self.attr_expression[name] = expression
        #     return attribute
        # else:
        #     raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')
    
    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return self.name == other or self.inhertance is not None and self.inhertance.conforms_to(other)

    def bypass(self):
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type: Type = return_type
        self.body = None
        #self.params_values = None

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Scope:
    def __init__(self, parent=None):
        self.local_variables = set()
        self.functions: dict[str, List[Method]] = {} # {key: id, valor: len(parameters)}
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.local_variables)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.local_variables.add(info)
        return info

    def find_local_variable(self, vname, index=None):
        locals = self.local_variables if index is None else itt.islice(self.local_variables, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return None

    def find_variable(self, vname, index=None):
        locals = self.local_variables if index is None else itt.islice(self.local_variables, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if not self.parent is None else None
        
    def find_functions(self, vname, index=None):
        try:
            return self.functions[vname]
        except:
            return self.parent.find_functions(vname, self.index) if not self.parent is None else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.local_variables if x.name == vname)
    
    def method_is_define(self, vname, params_num):
        try:
            methods = [method for method in self.functions[vname] if len(method.param_names) == params_num]
            return len(methods) != 0
        except:
            raise SemanticError(f'La funcion {vname} no esta definida')
        
    def get_method(self, vname, params_num):
        try:
            methods = [method for method in self.functions[vname] if len(method.param_names) == params_num]
            return methods[0]
        except:
            raise SemanticError(f'La funcion {vname} no esta definida')
    
class Context:
    def __init__(self):
        self.types: dict[str, Type] = {}

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
