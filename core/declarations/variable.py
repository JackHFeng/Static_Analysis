from slither.core.variables.local_variable import LocalVariable as Slither_Local_Variable


class Variable:
    def __init__(self):
        self._name = None
        self._type = None

    ###################################################################################
    ###################################################################################
    # region => public getters
    ###################################################################################
    ###################################################################################

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def __str__(self):
        return self.__class__.__name__ + ": " + self.name + "=>" + self.type

    def __repr__(self):
        return self.__class__.__name__ + ": " + self.name + "=>" + self.type

    # end of region
    ###################################################################################
    ###################################################################################
    # region => public getters
    ###################################################################################
    ###################################################################################

