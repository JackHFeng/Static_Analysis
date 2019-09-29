class Contract:
    def __init__(self):
        self.name = ''

        self.functions = {}
        self.state_variables = {}
        self.modifiers = {}

    def get_functions(self):
        return self.functions.values()

    def get_state_variables(self):
        return self.state_variables.values()

    def get_modifiers(self):
        return self.modifiers.values()


class Function:
    def __init__(self):
        self.name = ''
        self.signature = ''
        self.visibility = ''

        self.state_variables_written = []
        self.state_variables_read = []

        self.modifiers = []

        self.requires = []

        self.local_variables_read = []
        self.local_variables_written = []

    def get_state_variables_read(self):
        return self.state_variables_read

    def get_state_variables_written(self):
        return self.state_variables_written

    def get_state_variables_read(self):
        return self.state_variables_read

    def get_state_variables_written(self):
        return self.state_variables_written

    def get_requires(self):
        return self.requires

    def update_local_variables(self):
        for i, sv in enumerate(self.state_variables_read):
            for j, lv in enumerate(self.local_variables_read):
                if sv.name == lv.name:
                    del self.local_variables_read[j]

        for i, sv in enumerate(self.state_variables_written):
            for j, lv in enumerate(self.local_variables_written):
                if sv.name == lv.name:
                    del self.local_variables_written[j]


class Modifier:
    def __init__(self):
        self.name = ''
        self.visibility = ''

        self.state_variables_read = []
        self.state_variables_written = []  # Modifiers can write to state variables

        self.v_read = []
        self.v_written = []

        self.f_used = []

        self.requires = []

    def get_state_variables_read(self):
        return self.state_variables_read

    def get_state_variables_written(self):
        return self.state_variables_written

    def get_requires(self):
        return self.requires


class Variable:
    def __init__(self):
        self.name = ''
        self.type = ''

    def is_stateVariable(self):
        return False


class State_Variable(Variable):
    def __init__(self):
        super().__init__()
        self.visibility = ''
        self.initialized = False

        self.f_read = []
        self.f_written = []
        # self.f_write_conditions = []

        self.requires = []

    def is_stateVariable(self):
        return True

    def requires_appeared_in(self):
        return self.requires

    def functions_read(self):
        return self.f_read

    def functions_written(self):
        return self.f_written


class Require:
    def __init__(self):
        self.code = ''

        self.IRs = []

        self.local_variables_read = []
        self.local_variables_written = []

        self.state_variables_read = []
        self.state_variables_written = []

        self.operations = []

    def get_IRs(self):
        return self.IRs

    def get_local_variables_read(self):
        return self.local_variables_read

    def get_local_variables_written(self):
        return self.local_variables_written

    def get_state_variables_read(self):
        return self.state_variables_read

    def get_state_variables_written(self):
        return self.state_variables_written

    def get_operations(self):
        return self.operations

    def update_local_variables(self):
        for i, sv in enumerate(self.state_variables_read):
            for j, lv in enumerate(self.local_variables_read):
                if sv.name == lv.name:
                    del self.local_variables_read[j]

        for i, sv in enumerate(self.state_variables_written):
            for j, lv in enumerate(self.local_variables_written):
                if sv.name == lv.name:
                    del self.local_variables_written[j]


class Operation:
    def __init__(self):
        self.name = ''
        self.operator = ''


class BinaryOperation(Operation):
    def __init__(self):
        super().__init__()
        self.left
        self.right


class UnaryOperation(Operation):
    def __init__(self):
        super().__init__()
        self.var

