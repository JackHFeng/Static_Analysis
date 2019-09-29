from slither.core.declarations.function import Function as Slither_Function
from slither.core.declarations.modifier import Modifier as Slither_Modifier
from .function import Function
from .modifier import Modifier


class Contract:
    def __init__(self):
        self.name = ''

        self.functions = {}
        self.state_variables = {}
        self.modifiers = {}

    def get_functions(self):
        return self.functions.values()

    def get_state_variables(self):
        return self.state_variables.values()

    def get_modifiers(self):
        return self.modifiers.values()

    def create_function(self, function: Slither_Function):
        new_function = Function()
        print(f'Creating Function: {function.name}')
        new_function.name = function.name
        new_function.signature = function.signature_str
        new_function.visibility = function.visibility

        new_function.load_variables(function, self)

        self.functions[new_function.signature] = new_function

    def create_modifier(self, modifier: Slither_Modifier):
        new_modifier = Modifier()
        print(f'Creating Modifier: {modifier.name}')
        new_modifier.name = modifier.name
        new_modifier.visibility = modifier.visibility

        new_modifier.load_variables(modifier, self)

        self.modifiers[new_modifier.name] = new_modifier
