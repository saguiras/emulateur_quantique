
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
     from QETO.quantum_circuit import QCircuit



class Measurement:
    def __init__(self, measurements: list[int], qcircuit: 'QCircuit'):
         self.measurements = measurements
         self.qcircuit = qcircuit

    def __str__(self) -> str:
        assert self.qcircuit.nb_qubits
        out = f"QCircuit: {self.qcircuit.label}"
        for outcome, count in enumerate(np.bincount(self.measurements)):
                if count != 0:
                    binary_outcome = format(outcome, '0' + str(self.qcircuit.nb_qubits) + 'b').zfill(self.qcircuit.nb_qubits)
                    reversed_binary_outcome = binary_outcome[::-1]
                    out += f"\n Outcome {reversed_binary_outcome}: Count = {count}"
        return out