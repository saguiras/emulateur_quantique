import numpy as np

class Gates:
    def H(self, *target_qubit):
        # Apply the Hadamard gate to a single qubit
        h_gate = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]], dtype=complex)
        # Add the operation to the operations list
        self.apply_gate_qubit(h_gate, list(target_qubit),gate_name='H')

    
    def swap(self, qubit1, qubit2):
        # Create the SWAP gate matrix
        swap_gate = np.array([[1, 0, 0, 0],
                              [0, 0, 1, 0],
                              [0, 1, 0, 0],
                              [0, 0, 0, 1]], dtype=complex)

        # Apply the SWAP gate to the specified qubits
        self.apply_gate_qubit(swap_gate, [qubit1, qubit2],gate_name='swap')
    
    def X(self, *target_qubit):
        # Apply the Pauli-X gate to multiple qubits
        x_gate = np.array([[0, 1], [1, 0]], dtype=complex)
        self.apply_gate_qubit(x_gate, list(target_qubit), gate_name='X')

    def Y(self, *target_qubit):
        # Apply the Pauli-Y gate to a single qubit
        y_gate = np.array([[0, -1j], [1j, 0]], dtype=complex)
        self.apply_gate_qubit(y_gate, list(target_qubit),gate_name='Y')

    def Z(self, *target_qubit):
        # Apply the Pauli-Z gate to a single qubit
        z_gate = np.array([[1, 0], [0, -1]], dtype=complex)
        self.apply_gate_qubit(z_gate, list(target_qubit),gate_name='Z')

    def Rx(self, target_qubit, angle_theta):
        # Create the Rx rotation matrix
        rx_matrix = np.array([[np.cos(angle_theta / 2), -1j * np.sin(angle_theta / 2)],
                              [-1j * np.sin(angle_theta / 2), np.cos(angle_theta / 2)]], dtype=complex)
        
        self.apply_gate_qubit(rx_matrix, [target_qubit],gate_name='Rx')

    def Ry(self, target_qubit, angle_theta):
        # Create the Ry rotation matrix
        ry_matrix = np.array([[np.cos(angle_theta / 2), -np.sin(angle_theta / 2)],
                              [np.sin(angle_theta / 2), np.cos(angle_theta / 2)]], dtype=complex)
        
        self.apply_gate_qubit(ry_matrix, [target_qubit],gate_name='Ry')

    def Rz(self, target_qubit, angle_theta):
        # Create the Rz rotation matrix
        rz_matrix = np.array([[np.exp(-1j * angle_theta / 2), 0],
                              [0, np.exp(1j * angle_theta / 2)]], dtype=complex)
        
        self.apply_gate_qubit(rz_matrix, [target_qubit],gate_name='Rz')
    
    def U(self, target_qubit, theta, phi, lam):
        # Create the U gate matrix
        u_matrix = np.array([
            [np.cos(theta/2), -np.exp(1j*lam)*np.sin(theta/2)],
            [np.exp(1j*phi)*np.sin(theta/2), np.exp(1j*(phi+lam))*np.cos(theta/2)]
        ], dtype=complex)

        # Apply the U gate to the specified qubit
        self.apply_gate_qubit(u_matrix, [target_qubit],gate_name='U{theta},{phi},{lam}')
    
    def CNOT(self, control, target):
        x_gate = np.array([[0, 1], [1, 0]], dtype=complex)
        self.controlled_gate(control, target, x_gate, gate_name='CNOT')

    def CZ(self, control, target):
        z_gate = np.array([[1, 0], [0, -1]], dtype=complex)
        self.controlled_gate(control, target, z_gate, gate_name='CZ')
    
    def C_custom(self, control, target, gate):
        self.controlled_gate(control, target, gate, gate_name='CZ')

    def controlled_gate(self, control, target, gate_matrix,  gate_name='O'):
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
        if not (0 <= target < self.num_qubits) or not (0 <= control < self.num_qubits):
            raise ValueError("Invalid qubit index")

        I = np.eye(2)
        zero = np.array([[1, 0], [0, 0]])
        one = np.array([[0, 0], [0, 1]])


        control_matrix = zero if control == 0 else I
        target_matrix = one if control == 0 else (gate_matrix if target == 0 else I)
    
        for i in range(1, self.num_qubits):
            if i == control:
                target_matrix = np.kron(target_matrix, one)
            elif i == target:
                target_matrix = np.kron(target_matrix, gate_matrix)
            else:
                target_matrix = np.kron(target_matrix, I)

        for i in range(1, self.num_qubits):
            if i == control:
                control_matrix = np.kron(control_matrix, zero)
            else:
                control_matrix = np.kron(control_matrix, I)

        contorl_gate = control_matrix + target_matrix

        self.apply_gate(contorl_gate, [control, target], gate_name)

    def custom_gate(self, gate_matrix, target_qubits):
        # Add validation and noise handling here if needed
        self.apply_gate_qubit(gate_matrix, target_qubits)