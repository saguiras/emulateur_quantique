import numpy as np
from QETO.tools.utils import I2, Matrix

def controlled_gate(control: int, target: int, gate_matrix: Matrix) -> Matrix:
        """
        Constructs the matrix representation of a controlled gate.

        Parameters:
            control (int): The control qubit index (0-based).
            target (int): The target qubit index (0-based).
            num_qubits (int): The total number of qubits in the system.
            gate_matrix (numpy.ndarray): The matrix representing the gate to be controlled.

        Returns:
            numpy.ndarray: The matrix representation of the controlled gate.
        """
        nb_qubit = abs(control - target) + 1
        zero = np.array([[1, 0], [0, 0]], dtype=complex)
        one = np.array([[0, 0], [0, 1]], dtype=complex)


        control_matrix = zero if control == 0 else I2
        target_matrix = one if control == 0 else (gate_matrix if target == 0 else I2)
    
        for i in range(1, nb_qubit):
            if i == control:
                target_matrix = np.kron(target_matrix, one)
            elif i == target:
                target_matrix = np.kron(target_matrix, gate_matrix)
            else:
                target_matrix = np.kron(target_matrix, I2)

        for i in range(1, nb_qubit):
            if i == control:
                control_matrix = np.kron(control_matrix, zero)
            else:
                control_matrix = np.kron(control_matrix, I2)

        return control_matrix + target_matrix

def swap_gate(control: int, target: int) -> Matrix:
    """
    Constructs the matrix representation of a SWAP gate for two qubits in a multi-qubit system.

    Parameters:
        control (int): The first qubit index (0-based) to be swapped.
        target (int): The second qubit index (0-based) to be swapped.
        num_qubits (int): The total number of qubits in the system.

    Returns:
        numpy.ndarray: The matrix representation of the SWAP gate.
    """
    nb_qubits = abs(control - target) + 1
    # Total dimension of the system (2^num_qubits)
    dim = 2**nb_qubits

    # Initialize the SWAP gate matrix as an identity matrix
    swap_matrix = np.eye(dim, dtype=complex)

    # Loop through all possible basis states
    for i in range(dim):
        # Convert the basis state index to binary representation
        binary_state = list(format(i, f"0{nb_qubits}b"))

        # Swap the control and target qubit states
        binary_state[nb_qubits - control - 1], binary_state[nb_qubits - target - 1] = (
            binary_state[nb_qubits - target - 1],
            binary_state[nb_qubits - control - 1],
        )

        # Convert the swapped binary state back to an index
        swapped_index = int("".join(binary_state), 2)

        # Set the appropriate entry in the SWAP matrix
        swap_matrix[i, i] = 0
        swap_matrix[i, swapped_index] = 1

    return swap_matrix
