import numpy as np


class Simulator:

    def __init__(self, nEnvironment: int, interval: tuple = (15, 20), matrixA: np.ndarray = None,
                 matrixB: np.ndarray = None, arrayT: np.ndarray = None) -> None:
        """This method is the constructor of the Simulator class

        Args: nEnvironment: Integer value
              matrixA: Environment relationship matrix with float valus
              matrixB: Influence matrix of actuators in the environment
              arrayT: array of temperature in environment

        Return: None
        """
        self.__nEnvironment = nEnvironment
        self.__l, self.__h = interval
        self.__matrixA = self.__generate_matrixA_values() if matrixA is None else matrixA
        self.__matrixB = self.__generate_matrixB_values() if matrixB is None else matrixB
        self.__arrayT = self.__generate_arrayT_values() if arrayT is None else arrayT.T
        self.__memory = [self.__arrayT]
        

    @property
    def nEnvironment(self) -> int:
        """This method is a property used to return the number of environments        
        Args: None
        Return: number of environments        
        """        
        return self.__nEnvironment

    @property
    def matrixA(self) -> np.ndarray:
        """This method is a property used to return the matrix A       
        Args: None
        Return: Matrix A    
        """
        return self.__matrixA
    
    @property
    def matrixB(self) -> np.ndarray:
        """This method is a property used to return the matrix B        
        Args: None
        Return: Matrix B        
        """
        return self.__matrixB
  
    @property
    def arrayT(self) -> np.ndarray:
        """This method is a property used to return the array T    
        Args: None
        Return: Array of temperature      
        """
        return self.__arrayT

    @property
    def memory_list(self) -> np.ndarray:
        """This method is a property used to return the array T    
        Args: None
        Return: Array of temperature      
        """
        return self.__memory

    @property
    def high(self):
        """This method is a property used to return a High value of interval random temperature array.    
        Args: None
        Return: High interval value of random temperature array.       
        """
        return self.__h
    
    @property
    def low(self):
        """This method is a property used to return a Low value of interval random temperature array.   
        Args: None
        Return: Low value of interval random temperature array.      
        """
        return self.__l
                
    def __generate_matrixA_values(self) -> np.ndarray:
        """This method is used to initialize matrix A with random values in the range between [0,1]      
        Args: None
        Return: np.ndarray with dimensions (nEnvironment x nEnvironment) which represents the matrix A      
        """
        aux_matrixA_values = np.random.rand(self.__nEnvironment, self.__nEnvironment)
        for i in range(len(aux_matrixA_values)):
            for j in range(len(aux_matrixA_values[i])):
                if i == j:
                    aux_matrixA_values[i][j] = 1

        print("Initializing matrix A with random values and unit diagonal")         
        return aux_matrixA_values.tolist()

    def __generate_matrixB_values(self) -> np.ndarray:
        """This method is used to initialize diagonal matrix B representing the nth interaction 
        between the environment and the actuator.
        Args: None
        Return: diagonal np.ndarray with dimensions (nEnvironment x nEnvironment)      
        """
        print("Initializing the diagonal matrix B")
        return np.eye(self.__nEnvironment, dtype=float)
 
    def __generate_arrayT_values(self) -> np.ndarray:
        """This method is used to initialize array T with random values in the range between [15,35].
        Args: None
        Return: np.ndarray with dimensions (nEnvironment) which represents the array of Temperature      
        """
        print(f"Initializing the temperature array with random values between {self.__l} and {self.__h}")

        return np.random.randint(low=18, high=22, size=self.__nEnvironment).T


    def update_arrayT(self, arrayU) -> None:
        """This method is used to update the values of the array of Temperature
        Args: array with the new powers to reach the desired temperature
        Return: array T with updated values      
        """
        temp = np.empty(self.__nEnvironment)
        for i in range(len(temp)):
            for j in range(len(self.__matrixA[i])):
                temp[i] += (self.__matrixA[i][j]*(self.__arrayT[j] - self.__arrayT[i]))

            temp[i] += self.__matrixB[i][i]*arrayU[i]
            temp[i] = round(temp[i], 2)

        aux = self.__arrayT + temp  
        self.update_memory_list(aux)        
        self.__arrayT =+ aux
        return aux

    def update_arrayT2(self, arrayU) -> None:
            """This method is used to update the values of the array of Temperature
            Args: array with the new powers to reach the desired temperature
            Return: array T with updated values      
            """
            h = (self.nEnvironment)/1000
            k1 = np.empty(self.__nEnvironment)
            k2 = np.empty(self.__nEnvironment)
            temp = np.empty(self.__nEnvironment)
            for i in range(len(temp)):
                for j in range(len(self.__matrixA[i])):
                    k1[i] += (self.__matrixA[i][j]*(self.__arrayT[i] - self.__arrayT[j]))
                    k2[i] += (self.__matrixA[i][j] + h)*(self.__arrayT[i] - self.__arrayT[j])
                    temp[i] += (self.__matrixA[i][j]*(self.__arrayT[i] - self.__arrayT[j]))

                k1 += self.__matrixB[i][i]*arrayU[i]
                k2 += (self.__matrixB[i][i]+h)*arrayU[i]
            temp = temp + .5*(k1+k2)*h
            temp = temp.astype(int)
            self.update_memory_list(temp)
            return temp

    def update_memory_list(self, arrayT: np.ndarray) -> None:
        """this method is used to store in memory the array containing the temperature of the environments
        Args: instance of Simulator class
        Return: array T with updated values      
        """
        self.__memory.append(arrayT)

    def post_temperature_status(self) -> np.ndarray:
        """this method is used to post the sending of temperature information from the 
           control center to the simulator
        Args: instance of ControlCenter class
        Return: array T with updated values      
        """
        print("sending the temperature information of the environments")
        return self.__memory[-1]

    def get_arrayU(self, other) -> np.ndarray:
        """this method is used to request the sending of temperature information from the 
           control center to the simulator 
        Args: instance of ControlCenter class
        Return: array T with updated values      
        """
        return other.post_upadate_arrayU()
