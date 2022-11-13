import numpy as np


class Simulator:

    def __init__(self, nEnvironment: int, arrayU: np.ndarray, interval: tuple =(0, 10), matrixA: np.ndarray = None,
                 matrixB: np.ndarray = None, matrixP: np.ndarray = None, arrayT: np.ndarray = None) -> None:
        """This method is the constructor of the Simulator class

        Args: nEnvironment: Integer value
              interval: Tuple with integer values
              matrixA: Environment relationship matrix with float valus
              matrixB: Influence matrix of actuators in the environment

        Return: None
        """
        self.__nEnvironment = nEnvironment
        self.l, self.h = interval
        self.__matrixA = self.__generate_matrixA_values() if matrixA is None else matrixA
        self.__matrixB = self.__generate_matrixB_values() if matrixB is None else matrixB
        self.__matrixP = self.__generate_matrixP_values() if matrixP is None else matrixP
        self.__arrayT = self.__generate_arrayT_values() if arrayT is None else arrayT.T
        self.__arrayU = arrayU
        self.__memory = [self.__arrayT]

    @property
    def nEnvironment(self):
        """This method is a property used to return the number of environments        
        Args: None
        Return: number of environments        
        """        
        return self.__nEnvironment

    @property
    def matrixA(self):
        """This method is a property used to return the matrix A       
        Args: None
        Return: Matrix A    
        """
        return self.__matrixA
    
    @property
    def matrixB(self):
        """This method is a property used to return the matrix B        
        Args: None
        Return: Matrix B        
        """
        return self.__matrixB

    @property
    def matrixP(self):
        """This method is a property used to return the matrix P        
        Args: None
        Return: Matrix P       
        """
        return self.__matrixP
    
    @property
    def arrayU(self):
        """This method is a property used to return the array U        
        Args: None
        Return: Matrix P       
        """
        return self.__arrayU

    @property
    def arrayT(self):
        """This method is a property used to return the array T    
        Args: None
        Return: Matrix P       
        """
        return self.__arrayT

    @property
    def memory_list(self):
        return self.__memory
                
    def __generate_matrixA_values(self):
        """This method is used to initialize matrix A with random values in the range between [0,1]      
        Args: None
        Return: np.ndarray with dimensions (nEnvironment x nEnvironment) which represents the matrix A      
        """
        return np.random.rand(self.__nEnvironment, self.__nEnvironment)

    def __generate_matrixB_values(self):
        """This method is used to initialize diagonal matrix B representing the nth interaction 
        between the environment and the actuator.
        Args: None
        Return: diagonal np.ndarray with dimensions (nEnvironment x nEnvironment)      
        """
        return np.eye(self.__nEnvironment, dtype=float)
       

    def __generate_matrixP_values(self):
        """This method is used to initialize matrix A with random values in the range between [l,h],
        l and h have default values of 0 and 10 respectively.
        Args: None
        Return: np.ndarray with dimensions (nEnvironment x nEnvironment) which represents the matrix P     
        """
        random_matrix_float = np.random.rand(self.__nEnvironment, self.__nEnvironment)
        random_matriz_int = np.random.randint(low=self.l+1, high=self.h+1, size=(self.__nEnvironment, self.__nEnvironment))
        return random_matrix_float - random_matriz_int

    def __generate_arrayT_values(self):
        """This method is used to initialize array T with random values in the range between [15,35].
        Args: None
        Return: np.ndarray with dimensions (nEnvironment) which represents the array of Temperature      
        """
        return np.random.randint(low=15, high=35, size=self.__nEnvironment).T

    def update_arrayT(self):
        """This method is used to update the values of the array of Temperature
        Args: None
        Return: array T with updated values      
        """
        self.__arrayT = (np.dot(self.__matrixA, self.__arrayT) - np.dot(self.__matrixB, self.__arrayU))
        return self.arrayT

    def update_memory_list(self):
        return self.__memory.append(self.update_arrayT())

    def post_status_nEnvironment(self):            
        return self.__memory[-1]
