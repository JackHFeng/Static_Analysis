from slither.core.declarations.function import Function as Slither_Function
from slither.core.declarations.modifier import Modifier as Slither_Modifier
from slither.core.declarations.contract import Contract as Slither_Contract
from .function import Function
from .modifier import Modifier


class Contract:
    def __init__(self, contract: Slither_Contract):
        self.name = ''

        self.functions = {}
        self.state_variables = {}
        self.modifiers = {}

        print(f'Creating Contract: {contract.name}')

        self.name = contract.name

        for modifier in contract.modifiers:
            self.create_modifier(modifier)

        for function in contract.functions:
            self.create_function(function)

    def get_function_by_name(self, name):
        for function in self.functions:
            if function.name == name:
                return function
        return None

    def get_modifier_by_name(self, name):
        for modifier in self.modifiers:
            if modifier.name == name:
                return modifier
        return None

    def get_state_variable_by_name(self, name):
        for state_variable in self.state_variables:
            if state_variable.name == name:
                return state_variable
        return None

    def create_function(self, function: Slither_Function):
        new_function = Function(function, self)

        self.functions[new_function.signature] = new_function

    def create_modifier(self, modifier: Slither_Modifier):
        new_modifier = Modifier(modifier, self)

        self.modifiers[new_modifier.name] = new_modifier

    def __str__(self):
        res = ''
        res += f'Contract Name: {self.name}\n'
        res += f'\tState Variables:\n'

        for sv in self.state_variables.values():
            res += f'\t\t{str(sv)}\n'

        res += '\n\tModifiers: \n'

        for m in self.modifiers.values():
            res += f'\t\t{str(m)}\n'

        res += '\n\tFunctions: \n'

        for f in self.functions.values():
            res += f'\t\t{str(f)}\n'
        return res
