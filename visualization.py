import numpy as np
import matplotlib.pyplot as plt

class Visualization:
    def visualize_state(self):
        # Visualize the quantum state as a bar chart of probabilities
        probabilities = np.abs(self.state) ** 2
        num_states = len(probabilities)
        
        # Filter out probabilities that are 0 when self.num_qubits is greater than 6
        if self.num_qubits > 5:
            filtered_probabilities = [prob for prob in probabilities if prob > 0]
            # Corresponding state labels for non-zero probabilities
            state_labels = [bin(i)[2:].zfill(self.num_qubits) for i, prob in enumerate(probabilities) if prob > 0]
        else:
            filtered_probabilities = probabilities
            state_labels = [bin(i)[2:].zfill(self.num_qubits) for i in range(num_states)]

        plt.bar(state_labels, filtered_probabilities)
        plt.xlabel('Quantum State')
        plt.ylabel('Probability')
        plt.title('Quantum State Visualization')
        plt.xticks(rotation=90)
        plt.show()
    
    def visualize_measurement(self, measurements):
        # Convert measurements to binary
        binary_measurements = [format(outcome, '0' + str(self.num_qubits) + 'b') for outcome in measurements]
        
        if self.num_qubits < 6:
            # Generate all possible binary outcomes
            all_possible_outcomes = [format(i, '0' + str(self.num_qubits) + 'b') for i in range(2**self.num_qubits)]
            # Count the frequency of each measurement outcome
            counts = [binary_measurements.count(outcome) for outcome in all_possible_outcomes]
        else:
            all_possible_outcomes, counts = np.unique(measurements, return_counts=True)
            all_possible_outcomes = [format(i, '0' + str(self.num_qubits) + 'b') for i in all_possible_outcomes]

        

        # Convert counts to a NumPy array for element-wise division
        counts = np.array(counts)

        # Create labels for the measurement outcomes
        measurement_labels = [str(measurement) for measurement in all_possible_outcomes]

        # Plot the measurement probabilities as a bar chart
        plt.bar(measurement_labels, counts)
        plt.ylabel('Count')
        plt.title('Measurement')
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
            
                
        i = 0
        for operation in self.operations:
            gate_name, target_qubits = operation[0], operation[1]
            for index, qubit in enumerate(target_qubits):
                row_index = qubit
                column_index = i * 9 + state + 1
                if operation[3] and not index == len(target_qubits) - 1:
                    gate_name2 = '| '+ ' ' * int(len(gate_name)/2 - 1) + '*' + ' ' * int(len(gate_name)/2) + ' |'
                else:
                    gate_name2 = '| ' + gate_name + ' |'
                size_gate = len(gate_name2)
                circuit_grid[row_index][column_index + int((9 - size_gate)/2) :column_index + int((9 - size_gate)/2) + size_gate] = f'{gate_name2}'
            i += 1
                
        
        for row in range(num_rows):
            circuit_grid[row][0:4] = f'|{row}>'

         # Display the circuit diagram
        for row in circuit_grid:
            print(''.join(row))
        
    def print_mesurement(self, measurements):
        for outcome, count in enumerate(np.bincount(measurements)):
                if count != 0:
                    binary_outcome = format(outcome, '0' + str(self.num_qubits) + 'b').zfill(self.num_qubits)
                    reversed_binary_outcome = binary_outcome[::-1]
                    print(f"Outcome {reversed_binary_outcome}: Count = {count}")

