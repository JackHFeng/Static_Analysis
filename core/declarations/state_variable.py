from .variable import Variable
from slither.core.variables.state_variable import StateVariable as Slither_State_Variable


class StateVariable(Variable):
    def __init__(self, variable: Slither_State_Variable):
        self.name = variable.name
        self.type = str(variable.type)
        self.visibility = variable.visibility

        # Whether this state variable is initialized by hard code during deployment
        self.initialized = True if variable.initialized else False

        # If initialized by hard code during deployment, return default value
        # If None is returned, use default value of its type
        self.default_value = variable.expression.value if variable.expression else None

        # If this state variable can be set using constructor
        self.set_by_constructor = False

        self.functions_read = set()
        self.functions_written = set()
        # self.f_write_conditions = []
        self.modifiers_read = set()
        self.modifiers_written = set()

        # Why have this variable?
        self.requires_read = set()
        print(self.name)
        print(self.type)
        print(self.get_default_value_in_string())
        print(self.get_value_by_type(self.get_default_value_in_string()))

    def is_state_variable(self):
        return True

    def is_local_variable(self):
        return False

    def get_default_value_in_string(self):
        if self.default_value:
            return self.default_value
        if self.type.startswith('int') or self.type.startswith('uint'):
            return '0'
        elif self.type == 'bool':
            return 'false'
        elif self.type.startswith('byte'):
            return '0'
        elif self.type == 'string':
            return ''
        elif self.type == 'address':
            return '0'
        else:
            print(f'{self.name} not parsable')

    def get_value_by_type(self, v):
        if self.type.startswith('int') or self.type.startswith('uint'):
            return int(v)
        elif self.type == 'bool':
            if v == 'true':
                return True
            else:
                return False
        elif self.type == 'string':
            return str(v)
        elif self.type == 'address':
            return '0x' + v.zfill(40)

