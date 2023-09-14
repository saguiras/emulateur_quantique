import numpy as np
import matplotlib.pyplot as plt

class Visualization:
    def visualize_state(self):
        # Visualize the quantum state as a bar chart of probabilities
        probabilities = np.abs(self.state) ** 2
        num_states = len(probabilities)
        state_labels = [bin(i)[2:].zfill(self.num_qubits) for i in range(num_states)]

        plt.bar(state_labels, probabilities)
        plt.xlabel('Quantum State')
        plt.ylabel('Probability')
        plt.title('Quantum State Visualization')
        plt.xticks(rotation=90)
        plt.show()

    def visualize_circuit(self):
        # Calculate the number of columns and rows based on the number of qubits and operations
        state = int(self.num_qubits/10) + 3
        num_columns = (len(self.operations)) * 9 + state # Each operation takes 10 characters (including spaces)
        num_rows = self.num_qubits  # Add lines between qubits
        # Initialize an empty grid for the circuit diagram
        circuit_grid = [[' ' for _ in range(num_columns)] for _ in range(num_rows)]

        for row in range(num_rows):
            for columns in range(num_columns):
                circuit_grid[row][columns] = '-'
            
                

        for operation in self.operations:
            gate_name, target_qubits = operation[0], operation[1]
            for qubit in target_qubits:
                row_index = qubit
                column_index = (self.operations.index(operation)) * 9 + state + 1
                gate_name2 = '| ' + gate_name + ' |'
                size_gate = len(gate_name2)
                circuit_grid[row_index][column_index + int((9 - size_gate)/2) :column_index + int((9 - size_gate)/2) + size_gate] = f'{gate_name2}'
                
        
        for row in range(num_rows):
            circuit_grid[row][0:4] = f'|{row}>'

         # Display the circuit diagram
        for row in circuit_grid:
            print(''.join(row))