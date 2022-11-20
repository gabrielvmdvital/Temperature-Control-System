import numpy as np
import random
import matplotlib.pyplot as plt


class ControlCenter:

    def __init__(self, nEnvironment: int, potency_limit: float,  interval: tuple =(0, 10),  
                    matrixP: np.ndarray = None, arrayU: np.ndarray = None, Ttarget: int = None):

        self.__nEnvironment = nEnvironment
        self.potency_limit = potency_limit
        self.l, self.h = interval
        self.__arrayU = np.zeros(self.__nEnvironment, dtype=float) if arrayU is None else arrayU
        self.__Ttarget = np.full(self.__nEnvironment, 20).T if Ttarget is None else Ttarget
        self.__matrixP = self.__generate_matrixP_values() if matrixP is None else matrixP
        self.__memory_arrayT = []
        self.__memory_arrayU = []

    @property
    def arrayU(self) -> np.ndarray:
        """This method is a property used to return the array of potency.
        Args: None
        Return: number of environments
        """
        return self.__arrayU

    @property
    def nEnvironment(self) -> int:
        return self.__nEnvironment

    @property
    def memory_arrayT(self) -> np.ndarray:
        return self.__memory_arrayT

    @property
    def memory_arrayU(self) -> np.ndarray:
        return self.__memory_arrayU

    @property
    def Ttarget(self) -> np.ndarray:
        """This method is a property used to return the temperature of control
        Args: None
        Return: Temperature of control
        """
        return self.__Ttarget

    @property
    def matrixP(self) -> np.ndarray:
        """This method is a property used to return the matrix P        
        Args: None
        Return: Matrix P       
        """
        return self.__matrixP
    

    def update_arrayU(self, arrayT) -> np.ndarray:
        """This method is used to update the values of the array of Potency
        Args: None
        Return: array U with updated values
        """
        arrayU_limited = []
        self.__arrayU = np.round(
            self.__arrayU - self.__arrayU + np.dot(self.__matrixP, (self.__Ttarget - arrayT))
        )
        for potency in self.__arrayU:
            if potency > self.potency_limit:
                arrayU_limited.append(self.potency_limit)
            else:
                arrayU_limited.append(potency)

        return arrayU_limited
    
    def __generate_matrixP_values(self) -> np.ndarray:
        """This method is used to initialize matrix A with random values in the range between [l,h],
        l and h have default values of 0 and 10 respectively.
        Args: None
        Return: np.ndarray with dimensions (nEnvironment x nEnvironment) which represents the matrix P     
        """
        aux_matrix = np.eye(self.__nEnvironment, dtype=float)
        for i in range(len(aux_matrix)):
            for j in range(len(aux_matrix[i])):
                if i == j:
                    aux_matrix[i][j] = random.randint(1, 2) + random.random()
        
        return aux_matrix

    def post_upadate_arrayU(self) -> np.ndarray:
        return self.__memory_arrayU[-1]

    def get_arrayT(self, other) -> np.ndarray:
        return other.post_status_nEnvironment()

    def update_memory_arrayT_list(self, other) -> None:
        self.__memory_arrayT.append(self.get_arrayT(other))

    def update_memory_arrayU_list(self) -> None:
        self.__memory_arrayU.append(
            self.update_arrayU(self.__memory_arrayT[-1], self.__Ttarget)
        )

    
    def organize_dataMemory_list_to_plot(self) -> np.ndarray:
        """This method is used to gather data from of n-ésimo enviroments      
        Args: None
        Return: tuple of np.ndarray containing temperature and power data for each environment      
        """
        return np.column_stack(self.__memory_arrayT), np.column_stack(self.__memory_arrayU)