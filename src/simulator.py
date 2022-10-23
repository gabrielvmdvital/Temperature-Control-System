import numpy as np


class Simulator():
    def __init__(self, nEnvironment: int, interval: tuple =(0, 10),matrixA: np.ndarray = None, matrixB: np.ndarray = None, matrixP: np.ndarray = None) -> None:
        """This method is the constructor of the Simulator class

        Args: nEnvironment: Integer value
              interval: Tuple with integer values
              matrixA: Environment relationship matrix with float valus
              matrixB: Influence matrix of actuators in the environment

        Return: None
        """
        self._nEnvironment = nEnvironment
        self.l, self.h = interval
        self._matrixA = self.__generate_matrixA_values() if matrixA is None else matrixA
        self._matrixB = self.__generate_matrixB_values() if matrixB is None else matrixB
        self._matrixP = self.__generate_matrixP_values() if matrixP is None else matrixP

    @property
    def nEnvironment(self):
        """This method is a property used to return the number of environments        
        Args: None
        Return: number of environments        
        """        
        return self._nEnvironment

    @property
    def matrixA(self):
        """This method is a property used to return the matrix A       
        Args: None
        Return: Matrix A    
        """
        return self._matrixA
    
    @property
    def matrixB(self):
        """This method is a property used to return the matrix B        
        Args: None
        Return: Matrix B        
        """
        return self._matrixB

    @property
    def matrixP(self):
        """This method is a property used to return the matrix P        
        Args: None
        Return: Matrix P       
        """
        return self._matrixP
        
    def __generate_matrixA_values(self):
        """This method is used to initialize matrix A with random values in the range between [0,1]      
        Args: None
        Return: np.ndarray with dimensions (nEnvironment x nEnvironment) which represents the matrix A      
        """
        return np.random.rand(self._nEnvironment, self._nEnvironment)

    def __generate_matrixB_values(self):
        """This method is used to initialize diagonal matrix B representing the nth interaction 
        between the environment and the actuator.
        Args: None
        Return: diagonal np.ndarray with dimensions (nEnvironment x nEnvironment)      
        """
        return np.eye(self._nEnvironment, dtype=float)
       

    def __generate_matrixP_values(self):
        """This method is used to initialize matrix A with random values in the range between [l,h],
        l and h have default values of 0 and 10 respectively.
        Args: None
        Return: np.ndarray with dimensions (nEnvironment x nEnvironment) which represents the matrix B     
        """
        random_matrix_float = np.random.rand(self._nEnvironment, self._nEnvironment)
        random_matriz_int = np.random.randint(low=self.l, high=self.h, size=(self._nEnvironment, self._nEnvironment))
        return random_matrix_float - random_matriz_int

    def update_matrixA(self):
        """This method is used to update the values of the matrix
        Args: None
        Return: matrix A with updated values      
        """
        pass

    def update_matrixB(self):
        """This method is used to update the values of the matrix
        Args: None
        Return: matrix B with updated values      
        """
        pass

    def setup(self):
        while True:
            pass
