class Contract:
    def __init__(self):
        self.name = ''
        self.functions = []
        self.state_variables = []
        self.modifiers = []


class Function:
    def __init__(self):
        self.name = ''
        self.sv_written = []
        self.sv_read = []
        self.modifiers = []
        self.visibility = ''
        self.requires = []
        self.msg_values = []


class State_Variable:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.f_written = []
        self.f_write_conditions = []
        self.f_read = []
        self.m_read = []


class Modifier:
    def __init__(self):
        self.name = ''
        self.sv_read = []
        # self.sv_written # Can modifiers write to state variables? Likely Not, but need confirm
        self.f_used = []



