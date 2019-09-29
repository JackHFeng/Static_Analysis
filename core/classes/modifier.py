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