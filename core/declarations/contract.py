from slither.core.declarations.function import Function as Slither_Function
from slither.core.declarations.modifier import Modifier as Slither_Modifier
from slither.core.declarations.contract import Contract as Slither_Contract
from .function import Function
from .modifier import Modifier


class Contract:
    """
    Contract object.

    *** To be completed.
        default_satisfied_functions attribute is still yet to be loaded.
    """
    def __init__(self, contract: Slither_Contract):
        """
        *** To be completed.
            default_satisfied_functions attribute is still yet to be loaded.
        """

        # e.g. "Ballot".
        self.name = contract.name

        # map of functions with their name as key.
        self.functions = {}

        # map of state variables with their name as key.
        self.state_variables = {}

        # map of modifiers with their name as key.
        self.modifiers = {}

        # functions that can be executed right after contract deployment,
        # because their requires can be satisfied at the Initial state.
        self.default_satisfied_functions = []

        # create modifier objects.
        for modifier in contract.modifiers:
            self.create_modifier(modifier)

        # create function objects.
        for function in contract.functions:
            self.create_function(function)

    def get_function_by_name(self, name):
        """
        Getter function for getting a function object
        using its name, if function does not exist
        None will be returned.

        Finished.
        """
        return self.functions.get(name)

    def get_modifier_by_name(self, name):
        """
        Getter function for getting a modifier object
        using its name, if modifier does not exist
        None will be returned.

        Finished.
        """
        return self.modifiers.get(name)

    def get_state_variable_by_name(self, name):
        """
        Getter function for getting a state variable object
        using its name, if state variable does not exist
        None will be returned.

        Finished.
        """
        return self.state_variables.get(name)

    def create_function(self, function: Slither_Function):
        """
        Creates a function object, then adds to the map.

        Finished.
        """
        new_function = Function(function, self)

        self.functions[new_function.name] = new_function

    def create_modifier(self, modifier: Slither_Modifier):
        """
        Creates a modifier object, then adds to the map.

        Finished.
        """
        new_modifier = Modifier(modifier, self)

        self.modifiers[new_modifier.name] = new_modifier

    def __str__(self):
        """
        Overrides the str().

        Finished.
        """
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
