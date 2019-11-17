from .variable import Variable
from slither.core.variables.state_variable import StateVariable as Slither_State_Variable


class StateVariable(Variable):
    """
    State variable object.

    *** To be completed.
        During the stage of setting and getting the default value, more data type needs to be handled.
        What to do when modifier writes to the state variable?
        What is f_write_conditions attribute for? Saw it in slither somewhere, probably in the printers.
    """
    def __init__(self, variable: Slither_State_Variable):
        ### e.g. "balance".
        self.name = variable.name

        ### e.g. "mapping(uint256 => bool)", etc.
        self.type = str(variable.type)

        ### e.g."internal", "public" ,etc.
        self.visibility = variable.visibility

        ### whether this state variable is initialized by hard code during deployment.
        self.initialized = True if variable.initialized else False

        ### if this state variable can be set using constructor.
        self.set_by_constructor = False

        ### functions that read the current state variable.
        ### specifically, read by requires.
        self.functions_read = set()

        ### functions that writes to the current state variable.
        self.functions_written = set()

        ### saw this somewhere in slither, may need more investigation to
        ### find out about what it does exactly.
        # self.f_write_conditions = []

        ### modifiers that read the current state variable.
        self.modifiers_read = set()

        ### modifiers that writes to the current state variable.
        ### this doesn't often happen.
        ### but when it does, it's not handdled....😒
        """
        *** To be completed
            What to do when a modifier writes to a state variable? 
            How does it affect the dependency graph? 
        """
        self.modifiers_written = set()

        ### requires that read the current state variable.
        ### this attribute is not currently used, and may never be used...
        ### I'm just gonna leave it here in case it is needed in the future...smh
        self.requires_read = set()

        ### if initialized by hard code during deployment, return default value.
        ### if None is returned, use default value of its type.
        self.default_value = self.set_default_value(variable.expression.value if variable.expression else None)

        print(self.name)
        print(self.type)

    def is_state_variable(self):
        return True

    def is_local_variable(self):
        return False

    def set_default_value(self, _value):
        """
        Sets the default value of the state variable.

        *** To be completed.
            Handling more types.
        """
        default_value = default_value_helper(_value, self.type, self.name)

        if self.type.startswith('int') or self.type.startswith('uint'):
            return int(default_value)
        elif self.type == 'bool':
            if default_value == 'true':
                return True
            else:
                return False
        elif self.type == 'string' or self.type == 'byte' or self.type == 'address':
            return default_value
        else:
            raise Exception(f'Unhandled type: <{self.type}> for "{self.name}"')

    def has_default_value(self):
        """
        Check if state variable has a default value.
        If a state variable needs be set by constructor, then it does not have a default value.
        """
        return not self.set_by_constructor

    def get_default_value(self):
        """
        Getting the default value of the state variable.
        Must call has_default_value() first.
        """
        if self.set_by_constructor:
            raise Exception(f'"{self.name}"" does not have a default value because it needs to be set by constructor. '
                            f'Please call "has_default_value()" prior to calling "get_default_value()"')
        else:
            return self.default_value



### static utility functions
def default_value_helper(_value, _type, _name):
    """
    Helper for getting the default value of the state variable.
    If there is a default value statically assigned to the state variable, return default value.
    Otherwise, return the corresponding default solidity value for the data type.

    *** To be completed.
        Handling more types.
    """

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
        print(f'Unhandled type: {_type} for {_name}')
        pass

        # raise Exception(f'Unhandled type: {_type} for {_name}')

