from classes import *
import globals
from slither.core.declarations.function import Function as Slither_Function
from slither.core.declarations.modifier import Modifier as Slither_Modifier
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.variable import Variable as Slither_Variable


def createContract():
    for contract in globals.slither.contracts:
        n_contract = Contract()
        globals.contracts.append(n_contract)

        n_contract.name = contract.name

        for function in contract.functions:
            createFunction(function, n_contract)

        for modifier in contract.modifiers:
            createModifier(modifier, n_contract)


def createFunction(function: Slither_Function, n_contract: Contract):
    n_function = Function()

    n_function.name = function.name
    n_function.signature = function.signature_str
    n_function.visibility = function.visibility

    loadVariables(function, n_function, n_contract)

    n_contract.functions[n_function.signature] = n_function


def createModifier(modifier: Slither_Modifier, n_contract: Contract):
    n_modifier = Modifier()

    n_modifier.name = modifier.name
    n_modifier.visibility = modifier.visibility

    loadVariables(modifier, n_modifier, n_contract)

    n_contract.modifiers[n_modifier.name] = n_modifier


def loadVariables(function: Slither_Function, n_function: Function, n_contract: Contract):
    for variable in function.state_variables_read:
        if variable.name in n_contract.state_variables:
            n_variable = n_contract.state_variables[variable.name]
        else:
            n_variable = createStateVariable(variable)
            n_contract.state_variables[variable.name] = n_variable
        n_function.sv_read.append(n_variable)
        n_variable.f_read.append(n_function)

    for variable in function.state_variables_written:
        if variable.name in n_contract.state_variables:
            n_variable = n_contract.state_variables[variable.name]
        else:
            n_variable = createStateVariable(variable)
            n_contract.state_variables[variable.name] = n_variable
        n_function.sv_written.append(n_variable)
        n_variable.f_written.append(n_function)

    for variable in function.variables_read:
        n_variable = createVariable(variable)
        n_function.v_read.append(n_variable)

    for variable in function.variables_written:
        n_variable = createVariable(variable)
        n_function.v_written.append(n_variable)


def createStateVariable(variable: Slither_StateVariable) -> State_Variable:
    n_variable = State_Variable()
    n_variable.name = variable.name
    n_variable.type = variable.type
    n_variable.visibility = variable.visibility
    n_variable.initialized = variable.initialized
    return n_variable


def createVariable(variable: Slither_Variable) -> Variable:
    n_variable = Variable
    n_variable.name = variable.name
    n_variable.type = variable.type

    return n_variable

