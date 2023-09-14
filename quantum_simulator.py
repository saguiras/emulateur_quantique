import numpy as np
from gates import Gates
from visualization import Visualization

class QuantumSimulator(Gates, Visualization):
    def __init__(self, num_qubits, noise_prob=0.0):
        self.num_qubits = num_qubits
        self.state = np.zeros(2 ** num_qubits, dtype=complex)
        self.state[0] = 1.0  # Initialize with the |0...0> state
        self.noise_prob = noise_prob  # Probability of applying noise
        self.operations = []

    def apply_gate_qubit(self, gate_matrix, target_qubits, gate_name='CustomGate'):
        for qubit in target_qubits:
            if qubit < 0 or qubit >= self.num_qubits:
                raise ValueError("Target qubit index is out of bounds")

        # Add the operation to the operations list
        self.operations.append((gate_name, target_qubits))

            # Check if the gate_matrix is compatible with the target qubits
        I2 = np.eye(2)

        for target in target_qubits:
            result = I2
            if 0 == target:
                result = gate_matrix

            for i in range(1,self.num_qubits):
                if i == target:
                    result = np.kron(result, gate_matrix)
                else:
                    result = np.kron(result, I2)
            
            self.state = np.dot(self.state, result)

    def apply_gate(self, gate_matrix, target_qubit, gate_name='CustomGate'):
        self.operations.append((gate_name, target_qubit))
        self.state = np.dot(self.state, gate_matrix)
    
    def measure(self, num_shots=1):
        # Perform a measurement on the current state
        probabilities = np.abs(self.state) ** 2
        normalized_probabilities = probabilities / np.sum(probabilities)  # Normalize the probabilities

        measured_state = np.random.choice(len(self.state), p=normalized_probabilities, size=num_shots)
        return measured_state

    def reset(self):
        self.state = np.zeros(2 ** self.num_qubits, dtype=complex)
        self.state[0] = 1.0

    def get_amplitudes(self):
        return self.state

    
 