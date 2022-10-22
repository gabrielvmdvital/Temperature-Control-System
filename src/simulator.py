import numpy as np


class Simulator():
    def __init__(self, nEnvironment, matrixA = None, matrixB = None) -> None:
        self._nEnvironment = nEnvironment
        self._matrixA = np.array() if matrixA is None else matrixA
        self._matrixB = np.array() if matrixB is None else matrixB

    @property
    def nEnvironment(self):
        return self._nEnvironment

    def setup(self):
        while True:
            pass
