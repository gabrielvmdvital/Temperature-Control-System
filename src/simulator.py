import numpy as np


class Simulator():
    def __init__(self, nEnvironment: int, interval: tuple =(0, 10),matrixA: np.ndarray = None, matrixB: np.ndarray = None) -> None:
        self._nEnvironment = nEnvironment
        self.low, self.high = interval
        self._matrixA = self.generate_matrixA_values() if matrixA is None else matrixA
        self._matrixB = self.generate_matrixB_values() if matrixB is None else matrixB

    @property
    def nEnvironment(self):
        return self._nEnvironment

    def generate_matrixA_values(self):
        return np.random.rand(self._nEnvironment, self._nEnvironment)

    def generate_matrixB_values(self, low, hight):
        random_matrix_float = np.random.rand(self._nEnvironment, self._nEnvironment)
        random_matriz_int = np.random.randint(self.low, self.high, size=(self._nEnvironment, self._nEnvironment))
        return random_matrix_float - random_matriz_int



    def setup(self):
        while True:
            pass
