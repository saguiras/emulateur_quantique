from __future__ import annotations
from typing import Optional

import numpy as np

from QETO.gate.generate_gate_matrix import controlled_gate, swap_gate
from QETO.tools.utils import Matrix, Number


class Gate:
    def __init__(self, matrix: Matrix, target: Optional[int | list[int]]):
        self.target = [target] if isinstance(target, int) else (target or [])
        self.matrix = matrix
    
    def __str__(self) -> str:
        return "Not implemented"

class ControlGate(Gate):
    def __init__(self, matrix: Matrix, control: int, target: int, ):
        #control = [control] if isinstance(control, int) else (control or [])
        #target = [target] if isinstance(target, int) else (target or [])
        #if set(target) & set(control):
        #    raise ValueError("Target qubit is also a control qubit")
        self.control = control
        super().__init__(matrix,target)

class ParameterGate(Gate):
    def __init__(self, matrix: Matrix, target: Optional[int | list[int]], parameter: Optional[Number | list[Number]]):
        if parameter is None:
            parameter = []
        elif isinstance(parameter, int):
            parameter = [parameter]
        self.parameter = parameter
        super().__init__(matrix, target)

class H(Gate):
    def __init__(self, target: Optional[int | list[int]]= None):
        matrix = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]], dtype=complex)
        super().__init__(matrix, target)

    def __str__(self) -> str:
        return "H"

class X(Gate):
    def __init__(self, target: Optional[int | list[int]] = None):
        # Apply the Pauli-X gate to multiple qubits
        matrix = np.array([[0, 1], [1, 0]], dtype=complex)
        super().__init__(matrix, target)
    
    def __str__(self) -> str:
        return "X"

class Y(Gate):
    def __init__(self, target: Optional[int | list[int]]= None):
        # Apply the Pauli-Y gate to a single qubit
        matrix = np.array([[0, -1j], [1j, 0]], dtype=complex)
        super().__init__(matrix, target)
    
    def __str__(self) -> str:
        return "Y"

class Z(Gate):
    def __init__(self, target: Optional[int | list[int]]= None):
        # Apply the Pauli-Z gate to a single qubit
        matrix = np.array([[1, 0], [0, -1]], dtype=complex)
        super().__init__(matrix, target)
    
    def __str__(self) -> str:
        return "Z"

class Rx(ParameterGate):
    def __init__(self, target: Optional[int | list[int]] = None, angle: Number = 0):
        # Create the Rx rotation matrix
        matrix = np.array([[np.cos(angle / 2), -1j * np.sin(angle / 2)],
                            [-1j * np.sin(angle / 2), np.cos(angle / 2)]], dtype=complex)
        self.angle = angle
        super().__init__(matrix, target, angle)
    
    def __str__(self) -> str:
        return f"Rz({round(self.angle, 2)})"

class Ry(ParameterGate):
    def __init__(self, target: Optional[int | list[int]] = None, angle: Number = 0):
        # Create the Ry rotation matrix
        matrix = np.array([[np.cos(angle / 2), -np.sin(angle / 2)],
                            [np.sin(angle / 2), np.cos(angle / 2)]], dtype=complex)
        self.angle = angle
        super().__init__(matrix, target, angle)
    
    def __str__(self) -> str:
        return f"Ry({round(self.angle, 2)})"

class Rz(ParameterGate):
    def __init__(self, target: Optional[int | list[int]] = None, angle: Number = 0):
        # Create the Rz rotation matrix
        matrix = np.array([[np.exp(-1j * angle / 2), 0],
                            [0, np.exp(1j * angle / 2)]], dtype=complex)
        self.angle = angle
        super().__init__(matrix, target, angle)
    
    def __str__(self) -> str:
        return f"Rz({round(self.angle, 2)})"

class U(ParameterGate):
    def __init__(self, target: Optional[int | list[int]] = None, theta: Number = 0, phi: Number= 0, lambd: Number= 0):
        # Create the U gate matrix
        matrix = np.array([
            [np.cos(theta/2), -np.exp(1j*lambd)*np.sin(theta/2)],
            [np.exp(1j*phi)*np.sin(theta/2), np.exp(1j*(phi+lambd))*np.cos(theta/2)]
        ], dtype=complex)
        self.theta = theta
        self.phi = phi
        self.lambd = lambd
        super().__init__(matrix, target, [theta, phi, lambd])
    
    def __str__(self) -> str:
        return f"U({round(self.theta, 2)},{round(self.phi, 2)},{round(self.lambd, 2)})"

class Swap(ControlGate):
    def __init__(self, control: int, target: int):
        matrix = swap_gate(control, target)
        super().__init__(matrix, control, target)
    
    def __str__(self) -> str:
        return "Swap"

class CNOT(ControlGate):
    def __init__(self, control: int, target: int):
        matrix = np.array([[0, 1], [1, 0]], dtype=complex)
        matrix = controlled_gate(control, target, matrix)
        super().__init__(matrix, control, target)
    
    def __str__(self) -> str:
        return "X"


class CZ(ControlGate):
    def __init__(self, control: int, target: int):
        matrix = np.array([[1, 0], [0, -1]], dtype=complex)
        matrix = controlled_gate(control, target, matrix)
        super().__init__(matrix, control, target)
    
    def __str__(self) -> str:
        return "Z"

class C_custom(ControlGate):
    def __init__(self, control: int, target: int, gate: Gate | Matrix):
        if isinstance(gate, Gate):
            gate = gate.matrix
        if len(gate[0]) != 2:
            raise ValueError("The gate matrix should be 2D.")
        matrix = controlled_gate(control, target, gate)
        super().__init__(matrix, target, control)
    
    def __str__(self) -> str:
        return "U"

class Custom(Gate):
    def __init__(self, target: int, matrix: Matrix):
        super().__init__(matrix, target)
    
    def __str__(self) -> str:
        return "U"
    
NATIVE_GATE = [H, X, Y, Z, Rx, Ry, Rz, CNOT, CZ, Swap, U]