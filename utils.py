from classes import *
import globals
from slither.core.declarations.function import Function as Slither_Function
from slither.core.declarations.modifier import Modifier as Slither_Modifier
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.variable import Variable as Slither_Variable





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



