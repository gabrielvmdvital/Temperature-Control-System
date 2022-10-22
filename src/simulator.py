import numpy as np


class Simulator():
    def __init__(self, nEnvironment, matrixA = None, matrixB = None) -> None:
        self._nEnvironment = nEnvironment
        if matrixA is None and matrixB is None:
            self._matrixA = np.array()
            self._matrixB = np.array()
        else:
            self._matrixA = matrixA
            self._matrixB = matrixB

    @property
    def nEnvironment(self):
        return self._nEnvironment

    def setup(self):
        while True:
            pass
