# QETO Quantum Emulator tools and Other

## Overview
QETO is a Python-based library designed to Emulate quantum circuits. It provides a suite of tools to create, visualize, and measure quantum circuits with ease. The library includes functionalities for generating random circuits, converting gates to matrix representations, and visualizing quantum states and measurements.

## Features
- **Quantum Circuit Creation**: Easily create and manipulate quantum circuits using built-in gate functions.
- **Visualization**: Visualize quantum circuits, states, and measurements with intuitive graphical representations.
- **Random Circuit Generation**: Generate random quantum circuits for testing and experimentation.
- **Matrix Conversion**: Convert quantum gates to their matrix representations.
- **Measurement**: Measure the quantum state of circuits and visualize the results.

## Installation
To install QETO, you need to clone the repository and install the necessary dependencies.

```bash
git clone https://github.com/saguiras/emulateur_quantique.git
cd emulateur_quantique
#pip install -r requirements.txt
```

## Usage
Below is an example script that demonstrates the basic usage of the QETO library.

### Example: `test.py`
```python
from QETO.gate.gate import *
from QETO.gate.generate_matrix_cicuit import gate_to_matrix_circuit
from QETO.quantum_circuit import QCircuit
from QETO.tools.generique import random_circuit
from QETO.tools.visualization import visualize_circuit, visualize_measurement, visualize_state

# Create a quantum circuit with 2 qubits
q = QCircuit(2)

# Add an X gate to the circuit
q.add(X())

# Run the circuit and obtain the state and matrix
state, matrix = q.run()
print(matrix)

# Visualize the quantum state
visualize_state(state)

# Visualize the quantum circuit
visualize_circuit(q)

# Measure the circuit and print the results
print(q.measure())

# Generate a random quantum circuit
q1 = random_circuit()
print(q1.gate)

# Visualize the random circuit
visualize_circuit(q1)

# Measure the random circuit and visualize the results
measure = q1.measure()
visualize_measurement(measure)
```
