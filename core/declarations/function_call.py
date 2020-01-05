from slither.core.declarations import SolidityFunction as Slither_SolidityFunction

from slither.solc_parsing.declarations.modifier import ModifierSolc as Slither_ModifierSolc
from slither.solc_parsing.declarations.function import FunctionSolc as Slither_FunctionSolc

from slither.core.declarations.function import Function as Slither_Function
from slither.core.declarations.modifier import Modifier as Slither_Modifier
from slither.core.declarations.solidity_variables import SolidityVariableComposed as Slither_SolidityVariableComposed
from slither.core.declarations.solidity_variables import SolidityVariable as Slither_SolidityVariable

from slither.slithir.operations import SolidityCall as Slither_SolidityCall
from slither.solc_parsing.cfg.node import NodeSolc as Slither_NodeSolc
from slither.solc_parsing.variables.local_variable import LocalVariableSolc

from .local_variable import LocalVariable
from .require import Require
from .state_variable import StateVariable
from .parameter import Parameter
from .solidity_variable import SolidityVariable
from .solidity_variable_composed import SolidityVariableComposed

require_functions = [Slither_SolidityFunction("require(bool)"),
                     Slither_SolidityFunction("require(bool,string)")]


class FunctionCall:
    def __init__(self):

        # e.g. "constructor".
        self._name = None

        # e.g. "constructor(bytes32[]) returns()".
        self._signature = None

        # contract object where current function belongs.
        self._parent_contract = None

        # set of requires.
        self._requires = set()

        # set of parameters.
        self._parameters = set()

        # source code of function, currently not available
        self._source_code = None

        # set of state variables written by the function.
        self._state_variables_written = set()

        # set of state variables read by the function.
        # specifically, read by the requires within the function.
        self._state_variables_read = set()

        # a dic for keeping all the necessary local variables
        self._local_variables = {}

        # local variables read by the function.
        # specifically, read by the requires within the function.
        self._local_variables_read = set()

        # local variables written by the function.
        self._local_variables_written = set()

        # hash of the function/modifier signature
        self._sig_hash = None

        # CT test cases
        self._test_cases = []

    ###################################################################################
    ###################################################################################
    # region => public getters
    ###################################################################################
    ###################################################################################

    @property
    def name(self):
        return self._name

    @property
    def signature(self):
        return self._signature

    @property
    def parent_contract(self):
        return self._parent_contract

    @property
    def requires(self):
        return list(self._requires)

    @property
    def parameters(self):
        return list(self._parameters)

    def add_parameter(self, parameter):
        self._parameters.add(parameter)

    # @property
    # def parameter_names(self):
    #     return ', '.join([p.name for p in self._parameters])

    @property
    def source_code(self):
        return self._source_code

    @property
    def state_variables_written(self):
        return list(self._state_variables_written)

    @property
    def state_variables_read(self):
        return list(self._state_variables_read)

    @property
    def local_variables(self):
        return self._local_variables.values()

    @property
    def local_variables_dic(self):
        return self._local_variables

    def add_local_variable(self, local_variable):
        self._local_variables[local_variable.name] = local_variable

    @property
    def local_variables_read(self):
        return list(self._local_variables_read)

    @property
    def local_variables_written(self):
        return list(self._local_variables_written)

    @property
    def sig_hash(self):
        return self._sig_hash

    @property
    def test_cases(self):
        return self._test_cases

    # end of region
    ###################################################################################
    ###################################################################################
    # region => public getters
    ###################################################################################
    ###################################################################################

    ###################################################################################
    ###################################################################################
    # region => private functions
    ###################################################################################
    ###################################################################################

    def _load_parameters(self, function_call):
        """
        Creating the parameter objects.

        Finished.
        """
        for variable in function_call.parameters:
            new_parameter = Parameter(variable)
            self._parameters.add(new_parameter)
            self.add_local_variable(new_parameter)

    def _load_variables(self, function_call):
        """
        Loading both local and state variable objects.

        Finished.
        """
        self._load_state_variables(function_call.state_variables_written, 'written')
        self._load_local_variables(function_call.variables_written, 'written')

    def _load_state_variables(self, variables, read_or_write):
        """
        Loading state variable objects.

        Finished.
        """
        for variable in variables:
            # get from dict if already exist
            if variable.name in self._parent_contract.state_variables_dic:
                new_variable = self._parent_contract.state_variables_dic[variable.name]
            else:
                new_variable = StateVariable(variable)
                self._parent_contract.state_variables_dic[variable.name] = new_variable

            # adding the current function/modifier into the state variable.
            new_variable.add_function_call(self.__class__.__name__.lower(), read_or_write, self)

            # adding the new state variable to the current function
            getattr(self, '_state_variables_' + read_or_write).add(new_variable)

    def _load_local_variables(self, variables, read_or_write):
        """
        Loading local variable object.

        Finished.
        """
        for variable in variables:
            # Slither_SolidityVariableComposed is msg.send etc.
            # There can be other types such as
            #       slither.solc_parsing.variables.local_variable_init_from_tuple.LocalVariableInitFromTupleSolc
            #           https://github.com/crytic/slither/blob/3e1f0d0a2fe8a8beb01121a6d3fc35b7bf033283/slither/core/variables/local_variable_init_from_tuple.py#L3
            #           It rarely happens
            #       slither.core.declarations.solidity_variables.SolidityVariable (such as evm time, "now")
            #           https://github.com/crytic/slither/blob/master/slither/core/declarations/solidity_variables.py

            # StateVariableSolc was in the following list, but has been removed
            # Because we are only loading local variable
            # At this moment, msg.sender, etc. are considered as local variables.
            if type(variable) not in [LocalVariableSolc, Slither_SolidityVariableComposed, Slither_SolidityVariable]:
                continue

            # There was a check of whether "variable" is None in the if condition
            # But has been removed.Why was there this check?

            if variable.name in self._local_variables:
                new_variable = self._local_variables[variable.name]
            else:
                new_variable = None
                if isinstance(variable, LocalVariableSolc):
                    new_variable = LocalVariable(variable)
                elif isinstance(variable, Slither_SolidityVariableComposed):
                    new_variable = SolidityVariableComposed(variable)
                    self.add_parameter(new_variable)
                elif isinstance(variable, Slither_SolidityVariable):
                    new_variable = SolidityVariable(variable)
                    self.add_parameter(new_variable)
                else:
                    raise Exception(f'Variable "{variable.name}" type "{type(variable)}" unhandled.')

                self.add_local_variable(new_variable)

            # duplicate has been checked.
            getattr(self, '_local_variables_' + read_or_write).add(new_variable)

    def _load_requires(self, function_call):
        """
        Loading front require objects in a function.

        Notes:
            ✔What about requires from calls to another function?
                ✔*** This is currently not considered since they are not the pre-conditional requires of the parent
                    function.

            ❌We need to differentiate requires that are not pre-conditions.
                Either requires that does not appear at the beginning of the function call, or post condition modifiers.
                This maybe achieved by using IR.
                    ✔*** requires doesn't appear at the beginning of the function call as been removed.
                    ❌*** post-conditional requires from modifiers due to _; still needs to be removed.

            ✔However, some requires might not appear at the beginning, yet they are still checking the pre-condition.
            ❌This is also indirect read of variables, which has not been handled.
                e.g.
                    sender = msg.sender;
                    require(owner == sender);
        """
        if type(function_call) in [Slither_Function, Slither_FunctionSolc]:
            for node in function_call.nodes:
                # https://github.com/crytic/slither/blob/master/slither/core/cfg/node.py
                # node_type => 0 represents Entry Point Node, we can safely skip this.
                # node_type => 19 (0x13 in hex) represents Variable Declaration, we can safely skip this because
                # requires appears after new variable declaration should still be pre-condition checking.
                if node.type in [0, 19]:
                    continue

                # require() is a internal call, this finds potential require statement.
                if node.internal_calls:
                    # check if the call is actually require call.
                    """
                    Multiple internal calls can happen within one node. 
                    Such as require(check())
                    Currently, this is still treated as normal precondition require. 
                    As long as there is a require call, this node is considered as a require. 
                    """
                    found_require = False
                    for internal_call in node.internal_calls:
                        if internal_call in require_functions:
                            self._create_require(node)
                            found_require = True
                            break

                    # if no require found after internal call.
                    # Later requires are deemed to be post condition checking
                    # And will be ignored.
                    if found_require:
                        continue
                    else:
                        break
                else:
                    # if not. Requires appear after this are not pre-conditional checking requires.
                    break
        elif type(function_call) in [Slither_Modifier, Slither_ModifierSolc]:
            """
            All requires from modifiers are been loaded regardless pre or post condition check. 
            """
            for ir in function_call.slithir_operations:
                if isinstance(ir, Slither_SolidityCall) and ir.function in require_functions:
                    self._create_require(ir.node)
        else:
            raise Exception(f'Unhandled function call type {type(function_call)}.')

    def _create_require(self, require: Slither_NodeSolc):
        """
        Creating require objects.

        *** To be completed.
            ❌There could be duplicate state or local variables added to the function.
                ✔There shouldn't be any duplicate state variables since they are only created once, and they are added to a set.
                There might be duplicate local variables.
            Because all state and local variables from modifier objects have already been loaded using load_modifiers().
            Take a look into this and confirm.
        """
        new_require = Require(require, self)

        # adding state variables read from the require to current function_call.
        for state_variable in new_require.state_variables_read:
            self._state_variables_read.add(state_variable)

        # adding local variables read from the require to current function_call.
        for local_variable in new_require.local_variables_read:
            self._local_variables_read.add(local_variable)

        self._requires.add(new_require)

    # end of region
    ###################################################################################
    ###################################################################################
    # region => private functions
    ###################################################################################
    ###################################################################################
