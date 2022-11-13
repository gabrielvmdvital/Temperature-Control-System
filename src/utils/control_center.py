import numpy as np
import matplotlib.pyplot as plt


class ControlCenter:

    def __init__(self, nEnvironment: int, potency_limit: float, arrayU: np.ndarray = None, Ttarget: int = None):
        self.__nEnvironment = nEnvironment
        self.potency_limit = potency_limit
        self.__arrayU = np.zeros(self.__nEnvironment, dtype=float) if arrayU is None else arrayU
        self.__Ttarget = np.full(self.__nEnvironment, 20).T if Ttarget is None else Ttarget
        self.__memory_arrayT = []
        self.__memory_arrayU = []

    @property
    def arrayU(self):
        """This method is a property used to return the array of potency.
        Args: None
        Return: number of environments
        """
        return self.__arrayU

    @property
    def nEnvironment(self):
        return self.__nEnvironment

    @property
    def memory_arrayT(self):
        return self.__memory_arrayT

    @property
    def memory_arrayU(self):
        return self.__memory_arrayU

    @property
    def Ttarget(self):
        """This method is a property used to return the temperature of control
        Args: None
        Return: Temperature of control
        """
        return self.__Ttarget

    def update_arrayU(self, arrayT, Ttarget):
        """This method is used to update the values of the array of Potency
        Args: None
        Return: array U with updated values
        """
        arrayU_limited = []
        self.__arrayU = np.round(
            self.__arrayU - self.__arrayU + np.dot(self.__matrixP, (self.__Ttarget - self.__arrayT))
        )
        for potency in self.__arrayU:
            if potency > self.potency_limit:
                arrayU_limited.append(self.potency_limit)
            else:
                arrayU_limited.append(potency)

        return arrayU_limited

    def post_upadate_arrayU(self):
        return self.__memory_arrayU[-1]

    def get_arrayT(self, other):
        return other.post_status_nEnvironment()

    def update_memory_arrayT_list(self):
        self.__memory_arrayT.append(self.get_arrayT())

    def update_memory_arrayU_list(self):
        self.__memory_arrayU.append(
            self.update_arrayU(self.__memory_arrayT[-1], self.__Ttarget)
        )
