from quantum_simulator import QuantumSimulator
import numpy as np

if __name__ == "__main__":
    num_qubits = 2  # Number of qubits (you can change this)
    simulator = QuantumSimulator(num_qubits, noise_prob=0.1)

    # Apply Hadamard gate to qubit 0
    simulator.H(0,1)
    simulator.X(0)
    simulator.H(0,1)

    simulator.visualize_circuit()

    simulator.optimize()

    simulator.visualize_circuit()

    simulator.apply_gate_all()
    # print(simulator.m.real)

    # Get the amplitudes of the quantum state
    amplitudes = simulator.get_amplitudes()

    #simulator.visualize_state()

    print("Amplitudes:\n", amplitudes)

    num_shots = 1 # Number of measurement repetitions
    measurements = simulator.measure(num_shots)

    #simulator.visualize_measurement(measurements)

    simulator.print_mesurement(measurements)