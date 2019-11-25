from .function import Function
from .modifier import Modifier
from .state_variable import StateVariable

from slither.core.declarations.function import Function as Slither_Function
from slither.core.declarations.modifier import Modifier as Slither_Modifier
from slither.core.declarations.contract import Contract as Slither_Contract


class Contract:
    """
    Contract object.

    *** To be completed.
    """
    def __init__(self, _contract: Slither_Contract):
        """
        *** To be completed.
            default_satisfied_functions attribute is still yet to be loaded.
        """

        # e.g. "Ballot".
        self.name = _contract.name

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
        for modifier in _contract.modifiers:
            self.create_modifier(modifier)

        # create function objects.
        """
        Slither has a inbuilt function called "slitherConstructorVariables". 
        This is a dummy function that holds the state variable declaration statements. 
        E.g. uint a = 0;
        
        However, if a state variable is only declared without value assignment, 
        it will not show up in the dummy function. 
        E.g. uint a;
        """
        for function in _contract.functions:
            # print(function.name)
            self.create_function(function)

    def get_function_by_name(self, _name: str) -> Function:
        """
        Getter function for getting a function object
        using its name, if function does not exist
        None will be returned.

        Finished.
        """
        return self.functions.get(_name)

    def get_modifier_by_name(self, _name: str) -> Modifier:
        """
        Getter function for getting a modifier object
        using its name, if modifier does not exist
        None will be returned.

        Finished.
        """
        return self.modifiers.get(_name)

    def get_state_variable_by_name(self, _name: str) -> StateVariable:
        """
        Getter function for getting a state variable object
        using its name, if state variable does not exist
        None will be returned.

        Finished.
        """
        return self.state_variables.get(_name)

    def create_function(self, _function: Slither_Function):
        """
        Creates a function object, then adds to the map.

        Finished.
        """
        new_function = Function(_function, self)

        self.functions[new_function.name] = new_function

    def create_modifier(self, _modifier: Slither_Modifier):
        """
        Creates a modifier object, then adds to the map.

        Finished.
        """
        new_modifier = Modifier(_modifier, self)

        self.modifiers[new_modifier.name] = new_modifier

    def __str__(self):
        """
        Returns contract name.

        Finished
        """
        return self.name

    def contract_summary(self):
        """
        Prints the summary of the contract.

        Finished.
        """
        from .utils import increase_indentation

        res = []
        res.append(f'Contract Name: {self.name}')

        s = ""
        for v in self.state_variables.values():
            s += v.name + ', '

        res.append(f'State Variables: {s[:-2]}')

        res.append(f'Modifiers: ')

        for m in self.modifiers.values():
            res.append(increase_indentation(m.modifier_summary()))
            res.append('')

        res.append(f'Functions: ')

        for f in self.functions.values():
            res.append(increase_indentation(f.function_summary()))
            res.append('')

        return '\n'.join(res)
