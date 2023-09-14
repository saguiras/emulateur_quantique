from quantum_simulator import QuantumSimulator
import numpy as np

if __name__ == "__main__":
    num_qubits = 3  # Number of qubits (you can change this)
    simulator = QuantumSimulator(num_qubits, noise_prob=0.1)

    # Apply Hadamard gate to qubit 0
    simulator.X(2,0,1)
    simulator.CNOT(2,1)


    # Get the amplitudes of the quantum state
    amplitudes = simulator.get_amplitudes()

    print("Amplitudes:\n", amplitudes)

    num_shots = 1  # Number of measurement repetitions
    measurements = simulator.measure(num_shots)

    # Count the measurement outcomes
    counts = np.bincount(measurements)

    amplitudes = simulator.get_amplitudes()

    simulator.visualize_circuit()

    for outcome, count in enumerate(counts):
        if count != 0:
            binary_outcome = format(outcome, '0' + str(simulator.num_qubits) + 'b').zfill(simulator.num_qubits)
            reversed_binary_outcome = binary_outcome[::-1]
            print(f"Outcome {reversed_binary_outcome}: Count = {count}")
