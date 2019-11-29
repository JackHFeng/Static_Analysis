from .variable import Variable
from slither.core.variables.state_variable import StateVariable as Slither_State_Variable
from slither.core.expressions.literal import Literal
from slither.core.expressions.identifier import Identifier

from slither.core.solidity_types.elementary_type import ElementaryType
from slither.core.solidity_types.user_defined_type import UserDefinedType
from slither.core.solidity_types.mapping_type import MappingType
from slither.core.solidity_types.array_type import ArrayType

class StateVariable(Variable):
    """
    State variable object.

    *** To be completed.
        ❌ Still need to add state variables that are not checked by require.
    """
    def __init__(self, variable: Slither_State_Variable):
        # e.g. "balance".
        self.name = variable.name

        # e.g. "mapping(uint256 => bool)", etc.
        self.type = str(variable.type)

        # e.g."internal", "public" ,etc.
        self.visibility = variable.visibility

        # whether this state variable is initialized by hard code during deployment.
        self.initialized = True if variable.initialized else False

        # if this state variable can be set using constructor.
        self.set_by_constructor = False

        # functions that read the current state variable.
        # specifically, read by requires.
        self.functions_read = set()

        # functions that writes to the current state variable.
        self.functions_written = set()

        # saw this somewhere in slither, may need more investigation to
        # find out about what it does exactly.
        """
        *** To be completed. 
            What is this about?
        """
        # self.f_write_conditions = []

        # modifiers that read the current state variable.
        self.modifiers_read = set()

        # modifiers that writes to the current state variable.
        # this doesn't often happen.
        # but when it does, it's not handdled....😒
        """
        *** To be completed.
            What to do when a modifier writes to a state variable? 
            How does it affect the dependency graph? 
        """
        self.modifiers_written = set()

        # requires that read the current state variable.
        # this attribute is not currently used, and may never be used...
        # I'm just gonna leave it here in case it is needed in the future...😒
        self.requires_read = set()

        # the default value of the state variable.
        # only available when state variable is not set by constructor.
        self.default_value = \
            set_default_value(variable.type, variable.expression if variable.expression else None, self.name)

        # print(self.name)
        # print(self.type)

    def is_state_variable(self):
        """
        Check if the current object is an instance of StateVariable.
        Overrides the same method in Variable class.

        Finished.
        """
        return True

    def is_local_variable(self):
        """
        Check if the current object is an instance of Variable.
        Overrides the same method in Variable class.

        Finished.
        """
        return False

    def has_default_value(self):
        """
        Check if state variable has a default value.
        If a state variable needs be set by constructor, then it does not have a default value.

        Finished.
        """
        return not self.set_by_constructor

    def get_default_value(self):
        """
        Getting the default value of the state variable.
        Must call has_default_value() first.

        Finished.
        """
        if self.set_by_constructor:
            raise Exception(f'"{self.name}"" does not have a default value because it needs to be set by constructor. '
                            f'Please call "has_default_value()" prior to calling "get_default_value()"')
        else:
            return self.default_value

# static utility functions

def set_default_value(_type, _exp, _name):
    """
    _type:      data type of the state variable.
    _exp:       expression of the static value assignment, such as  "msg.sender" for "owner = msg.sender".
    _name:      state variable name.

    Sets the default value of the state variable.
    A default value only exists when the state variable is not modified by the constructor.

    *** To be completed.
        Handling more types.
    """
    slither_type = _type
    _type = str(_type)

    if isinstance(_exp, Literal):
        # if _exp is int, convert the number of python code.
        # using eval is for the cases of "1e10"
        if 'int' in str(_exp.type):
            _exp = eval(str(_exp))
        # ❌ other types are still using string.
        else:
            _exp = _exp.value
    elif isinstance(_exp, Identifier):
        """
            ❌ Only msg.sender or now etc. can be used for initial assignment. 
            However, for customized struct, it may work differently. 
            also a = 0, b = a
            
            *** To be completed
        """
        _exp = None
    elif not _exp:
        """
            Makes the _exp None. 
            ❌ There might be other cases. 
        """
        _exp = eval(str(_exp))
    else:
        raise Exception(f"Some unhandled cases happened. \n\t Type of _exp is {type(_exp)}")

    default_value = default_value_helper(_exp, slither_type, _name)

    if _type.startswith('int') or _type.startswith('uint'):
        return int(default_value)
    elif _type == 'bool':
        if default_value == 'true':
            return True
        else:
            return False
    elif _type == 'string' or _type == 'byte' or _type == 'address':
        return default_value
    elif not default_value:
        return None
    else:
        raise Exception(f'Unhandled type: \n\t {_type}')


def default_value_helper(_value, _type, _name):
    """
    Helper for getting the default value of the state variable.
    If there is a default value statically assigned to the state variable, return default value.
    Otherwise, return the corresponding default solidity value for the data type.

    *** To be completed.
        Handling more types.
    """

    slither_type = _type
    _type = str(_type)

    # There can also be <class 'slither.core.solidity_types.user_defined_type.UserDefinedType'>
    if isinstance(slither_type, ElementaryType):
        if _value:
            return _value

        if _type.startswith('int') or _type.startswith('uint'):
            return '0'
        elif _type == 'bool':
            return 'false'
        elif _type == 'string':
            return ''
        elif _type == 'byte':
            return '0x0'
        elif _type == 'address':
            return '0x' + "".zfill(40)
        else:
            raise Exception(f'Unhandled Solidity Elementary Type. \n {_type} for {_name}')

    # this is only returning the default value of the deepest type of a mapping or array.
    elif isinstance(slither_type, MappingType) or isinstance(slither_type, ArrayType):
        default_value_helper(_value, get_deepest_type(slither_type), _name)
    elif isinstance(slither_type, UserDefinedType):
        print(f'Unhandled user defined type: \n\t{_type} for {_name}')
        return None


def get_deepest_type(_type):

    if isinstance(_type, MappingType):
        d_type = get_deepest_type(_type.type_to)
    elif isinstance(_type, ArrayType):
        d_type = get_deepest_type(_type.type)
    elif isinstance(_type, ElementaryType):
        d_type = _type
    elif isinstance(_type, UserDefinedType):
        d_type = _type
    else:
        raise Exception(f'Unhandled type: \n\t {type(_type)}')

    return d_type