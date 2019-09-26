from classes import *
import globals
from slither.core.declarations.function import Function as Slither_Function
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable


def createContract():
    for contract in globals.slither.contracts:
        n_contract = Contract()
        globals.contracts.append(n_contract)

        n_contract = contract.name

        for function in contract.functions:
            createFunction(function, n_contract)


def createFunction(function : Slither_Function, n_contract : Contract):
    n_function = Function()
    n_contract.function

    n_function.name = function.name
    for variable in function.variables_read:
        n_variable = createStateVariable()


def createModifier():
    pass


def createStateVariable(variable : Slither_StateVariable) -> State_Variable:
    n_variable = State_Variable()
    n_variable.name = variable.name
    n_variable.full_name = variable.full_name
    n_variable.signature = variable.signature_str
    n_variable.type = variable.type
    n_variable.visibility = variable.visibility
    return n_variable


