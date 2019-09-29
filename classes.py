class Contract:
    def __init__(self):
        self.name = ''

        self.functions = {}
        self.state_variables = {}
        self.modifiers = {}


class Function:
    def __init__(self):
        self.name = ''
        self.signature = ''
        self.visibility = ''

        self.sv_written = []
        self.sv_read = []

        self.modifiers = []

        self.requires = []

        self.v_read = []
        self.v_written = []


class Modifier:
    def __init__(self):
        self.name = ''
        self.visibility = ''

        self.sv_read = []
        self.sv_written = []  # Modifiers can write to state variables

        self.v_read = []
        self.v_written = []

        self.f_used = []


class State_Variable:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.visibility = ''
        self.initialized = False

        self.f_read = []
        self.f_written = []
        # self.f_write_conditions = []


class Variable:
    def __init__(self):
        self.name = ''
        self.type = ''


class Require:
    def __init__(self):
        self.code = ''

        self.v_read = []
        self.v_written = []

        self.sv_read = []
        self.sv_written = []



