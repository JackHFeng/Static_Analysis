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