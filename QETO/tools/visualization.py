import numpy as np
import matplotlib.pyplot as plt

from typing import TYPE_CHECKING

from QETO.gate.gate import ControlGate
from QETO.measure import Measurement

if TYPE_CHECKING:
     from QETO.quantum_circuit import QCircuit

def visualize_state(state):
    # Visualize the quantum state as a bar chart of probabilities
    probabilities = np.abs(state) ** 2
    nb_qubits = len(probabilities)
    
    # Filter out probabilities that are 0 when nb_qubits is greater than 6
    if nb_qubits > 5:
        filtered_probabilities = [prob for prob in probabilities if prob > 0]
        # Corresponding state labels for non-zero probabilities
        state_labels = [bin(i)[2:].zfill(nb_qubits) for i, prob in enumerate(probabilities) if prob > 0]
    else:
        filtered_probabilities = probabilities
        state_labels = [bin(i)[2:].zfill(nb_qubits) for i in range(nb_qubits)]

    plt.bar(state_labels, filtered_probabilities)
    plt.xlabel('Quantum State')
    plt.ylabel('Probability')
    plt.title('Quantum State Visualization')
    plt.xticks(rotation=90)
    plt.show()

def visualize_measurement(measurements: Measurement):
    nb_qubits = measurements.qcircuit.nb_qubits
    assert nb_qubits
    # Convert measurements to binary
    binary_measurements = [format(outcome, '0' + str(nb_qubits) + 'b') for outcome in measurements.measurements]
    
    if nb_qubits < 6:
        # Generate all possible binary outcomes
        all_possible_outcomes = [format(i, '0' + str(nb_qubits) + 'b') for i in range(2**nb_qubits)]
        # Count the frequency of each measurement outcome
        counts = [binary_measurements.count(outcome) for outcome in all_possible_outcomes]
    else:
        all_possible_outcomes, counts = np.unique(measurements.measurements, return_counts=True)
        all_possible_outcomes = [format(i, '0' + str(nb_qubits) + 'b') for i in all_possible_outcomes]

    

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

def visualize_circuit(qcircuit: 'QCircuit'):
    
    qcirc = qcircuit.hard_copy()
    assert qcirc.nb_qubits
    circuit_row = [f'|{row}>' for row in range(qcirc.nb_qubits)]
        
            
    for gate in qcircuit.gate:
        for target in gate.target:
            gate_str = '-| ' + str(gate) + ' |-'
            if isinstance(gate, ControlGate):
                max_col = max([len(circuit_row[index]) for index in range(min(gate.control, target), max(gate.control, target)+1)])
                print('target',target,'gate.control',gate.control)
                for index in range(min(gate.control, target), max(gate.control, target)+1):
                    circuit_row[index] += '-' * (max_col - len(circuit_row[index]))
                    print(circuit_row[index])
                    if index == gate.control:
                        circuit_row[index] +=  '-' * int(len(gate_str)/2) + '*' + '-' * int(len(gate_str)/2)
                    elif index != target:
                        circuit_row[index] +=  '-' * int(len(gate_str)/2) + '|' + '-' * int(len(gate_str)/2)

            circuit_row[target] += gate_str
    
    max_col = max([len(row) for row in circuit_row])
    for row in circuit_row:
            row += '-' * (max_col - len(row))
            print(''.join(row))
    

