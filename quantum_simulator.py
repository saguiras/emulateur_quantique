import numpy as np
from gates import Gates
from Gates_opti import Gates_opti
from visualization import Visualization
from optimization import Optimization

class QuantumSimulator(Gates_opti, Visualization, Optimization):
    def __init__(self, num_qubits, noise_prob=0.0):
        self.num_qubits = num_qubits
        self.state = np.zeros(2 ** num_qubits, dtype=complex)
        self.state[0] = 1.0  # Initialize with the |0...0> state
        self.noise_prob = noise_prob  # Probability of applying noise
        self.operations = []
        I2 = np.eye(2)
        result = I2
        for i in range(1,self.num_qubits):
            result = np.kron(result, I2)
        self.m = result

    def apply_gate_qubit(self, gate_matrix, target_qubits, gate_name='CustomGate'):
        for qubit in target_qubits:
            if qubit < 0 or qubit >= self.num_qubits:
                raise ValueError("Target qubit index is out of bounds")

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

    
    def apply_gate_all(self):
        for operation in self.operations:
            for qubit in operation[1]:
                if qubit < 0 or qubit >= self.num_qubits:
                    raise ValueError("Target qubit index is out of bounds")
            
            if operation[3]:
                self.state = np.dot(self.state, operation[2])
                self.m = np.dot(self.m, operation[2])
            else:
                # build matrix of same dimantion
                # Check if the gate_matrix is compatible with the target qubits
                I2 = np.eye(2)

                for target in operation[1]:
                    result = I2
                    if 0 == target:
                        result = operation[2]

                    for i in range(1,self.num_qubits):
                        if i == target:
                            result = np.kron(result, operation[2])
                        else:
                            result = np.kron(result, I2)
                    
                    self.state = np.dot(self.state, result)
                    self.m = np.dot(self.m, result)