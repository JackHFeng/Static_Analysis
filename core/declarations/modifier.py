from .function import Function
from slither.core.declarations.modifier import Modifier as Slither_Modifier


class Modifier(Function):
    def __init__(self, modifier: Slither_Modifier, new_contract):
        self.name = modifier.name
        self.signature = modifier.signature_str
        self.visibility = modifier.visibility
        self.from_contract = new_contract

        self.functions_used = set()

        self.requires = set()

        self.parameters = set()

        self.state_variables_written = set()
        self.state_variables_read = set()

        self.local_variables_read = set()
        self.local_variables_written = set()

        #print(f'Creating Modifier: {modifier.name}')

        self.load_parameters(modifier)
        self.load_variables(modifier)
        self.load_requires(modifier)

    def __str__(self):
        return self.signature

