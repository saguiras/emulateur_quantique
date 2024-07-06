from __future__ import annotations
from copy import deepcopy
from typing import Optional

import numpy as np

from QETO.gate.gate import Gate
from QETO.gate.generate_matrix_cicuit import gate_to_matrix_circuit
from QETO.measure import Measurement


class QCircuit:

    def __init__(
        self,
        instructions: Optional[int | Gate | list[Gate]] = None,
        nb_qubits: Optional[int] = None,
        label: str = "qcirc",
    ):
        self.gate: list[Gate] = []
        self.label = label
        if isinstance(instructions, int) or instructions is None:
            self.nb_qubits = instructions
        else:
            self.nb_qubits = nb_qubits
            self.add(instructions)

    def add(self, instruction: Gate | list[Gate]):
        if isinstance(instruction, Gate):
            if (
                self.nb_qubits
                and instruction.target != []
                and max(instruction.target) > self.nb_qubits
            ):
                raise ValueError("Instruction target qubit index is out of bounds")
            self.gate.append(instruction)
        else:
            for instruction in instruction:
                if (
                    self.nb_qubits
                    and instruction.target != []
                    and max(instruction.target) > self.nb_qubits
                ):
                    raise ValueError("Instruction target qubit index is out of bounds")
                self.gate.append(instruction)

    def run(self):
        qcircuit = self.hard_copy()
        assert qcircuit.nb_qubits
        final_state = np.zeros(2**qcircuit.nb_qubits, dtype=complex)
        final_state[0] = 1.0
        final_matrix = np.eye(2**qcircuit.nb_qubits, dtype=complex)
        for gate in qcircuit.gate:
            matrix = gate_to_matrix_circuit(qcircuit, gate)
            final_matrix = np.dot(final_matrix, matrix)
            final_state = np.dot(final_matrix, final_state)
        return final_state, final_matrix

    def measure(self, num_shots: int = 100):
        # Perform a measurement on the current state
        state, _ = self.run()
        probabilities = np.abs(state) ** 2
        normalized_probabilities = probabilities / np.sum(
            probabilities
        )  # Normalize the probabilities

        measured_state = np.random.choice(
            len(state), p=normalized_probabilities, size=num_shots
        )
        return Measurement(measured_state.tolist(), self.hard_copy())

    def hard_copy(self) -> QCircuit:
        new_circuit = deepcopy(self)
        new_circuit.nb_qubits = (
            max(max(gate.target) for gate in new_circuit.gate) + 1
            if new_circuit.nb_qubits is None
            else new_circuit.nb_qubits
        )
        for gate in self.gate:
            if gate.target == []:
                gate.target = list(range(new_circuit.nb_qubits))
        return new_circuit
