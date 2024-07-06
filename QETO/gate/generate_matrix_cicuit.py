import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from QETO.quantum_circuit import QCircuit

import numpy as np
from QETO.gate.gate import ControlGate, Gate
from QETO.tools.utils import I2


def gate_to_matrix_circuit(qcircuit: "QCircuit", gate: Gate):
    assert qcircuit.nb_qubits
    final_matrix = matrix = np.eye(2**qcircuit.nb_qubits, dtype=complex)
    for target in gate.target:
        matrix = I2
        if target == 0 or (isinstance(gate, ControlGate) and gate.control == 0):
            matrix = gate.matrix

        for i in range(int(math.log2(gate.matrix.shape[0])), qcircuit.nb_qubits):
            if i == target or (isinstance(gate, ControlGate) and gate.control == i):
                matrix = np.kron(matrix, gate.matrix)
            else:
                matrix = np.kron(matrix, I2)
        final_matrix = np.dot(final_matrix, matrix)
    return final_matrix
