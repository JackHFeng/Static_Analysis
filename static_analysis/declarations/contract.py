from slither.core.declarations.contract import Contract as Slither_Contract
from slither.core.declarations.function import Function as Slither_Function
from slither.core.declarations.modifier import Modifier as Slither_Modifier

from .function import Function
from .modifier import Modifier
from .state_variable import StateVariable


class Contract:
    """
    Contract object.

    *** To be completed.
    """

    def __init__(self, contract: Slither_Contract):
        """
        *** To be completed.
            default_satisfied_functions attribute is still yet to be loaded.
        """

        # e.g. "Ballot".
        self._name = None

        # map of functions with their name as key.
        self._functions = {}

        # map of state variables with their name as key.
        self._state_variables = {}

        # map of modifiers with their name as key.
        self._modifiers = {}

        # functions that can be executed right after contract deployment,
        # because their requires can be satisfied at the Initial state.
        self._default_satisfied_functions = set()

        self._setter(contract)

    @property
    def name(self):
        return self._name

    @property
    def functions(self):
        return self._functions

    @property
    def state_variables(self):
        return self._state_variables

    @property
    def modifiers(self):
        return self._modifiers

    @property
    def default_satisfied_functions(self):
        return list(self._default_satisfied_functions)

    def add_default_sat_function(self, function):
        self._default_satisfied_functions.add(function)

    def _setter(self, contract: Slither_Contract):
        self._name = contract.name

        # create modifier objects.
        for modifier in contract.modifiers:
            self._create_modifier(modifier)

        # create function objects.
        """
        Slither has a inbuilt function called "slitherConstructorVariables". 
        This is a dummy function that holds the state variable declaration statements. 
        E.g. uint a = 0;

        However, if a state variable is only declared without value assignment, 
        it will not show up in the dummy function. 
        E.g. uint a;
        """
        for function in contract.functions:
            # print(function.name)
            self._create_function(function)

    def get_function_by_name(self, name: str) -> Function:
        """
        Getter function for getting a function object
        using its name, if function does not exist
        None will be returned.

        Finished.
        """
        return self._functions.get(name)

    def get_modifier_by_name(self, name: str) -> Modifier:
        """
        Getter function for getting a modifier object
        using its name, if modifier does not exist
        None will be returned.

        Finished.
        """
        return self._modifiers.get(name)

    def get_state_variable_by_name(self, name: str) -> StateVariable:
        """
        Getter function for getting a state variable object
        using its name, if state variable does not exist
        None will be returned.

        Finished.
        """
        return self._state_variables.get(name)

    def _create_function(self, function: Slither_Function):
        """
        Creates a function object, then adds to the map.

        Finished.
        """
        new_function = Function(function, self)

        self._functions[new_function.name] = new_function

    def _create_modifier(self, modifier: Slither_Modifier):
        """
        Creates a modifier object, then adds to the map.

        Finished.
        """
        new_modifier = Modifier(modifier, self)

        self._modifiers[new_modifier.name] = new_modifier

    def __str__(self):
        """
        Returns contract name.

        Finished
        """
        return self._name

    def contract_summary(self):
        """
        Prints the summary of the contract.

        Finished.
        """
        from .utils import increase_indentation

        res = list()
        res.append(f'Contract Name: {self._name}')

        res.append(f'State Variables: ')
        for v in self._state_variables.values():
            res.append(f'\t{v.name}({v.type}): {v.default_value}')
            res.append(f'\t\tinitialized: {v.initialized}')
            res.append(f'\t\tset by constructor: {v.set_by_constructor}')
            res.append(f'\t\tset by deployment: {v.set_by_deployment}')
            if v.set_by_deployment:
                res.append(f'\t\t\tusing: {v.var_used_in_deployment}')
        res.append('')

        res.append(f'Modifiers: ')

        for m in self._modifiers.values():
            res.append(increase_indentation(m.modifier_summary()))
            res.append('')

        res.append(f'Functions: ')

        for f in self._functions.values():
            res.append(increase_indentation(f.function_summary()))
            res.append('')

        return '\n'.join(res)
