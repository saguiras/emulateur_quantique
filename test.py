from QETO.gate.gate import *
from QETO.gate.generate_matrix_cicuit import gate_to_matrix_circuit
from QETO.quantum_circuit import QCircuit
from QETO.tools.generique import random_circuit
from QETO.tools.visualization import visualize_circuit, visualize_measurement, visualize_state


q = QCircuit(2)
q.add(X())

state, matrix = q.run()
print(matrix)
visualize_state(state)
visualize_circuit(q)
print(q.measure())

q1 = random_circuit()
print(q1.gate)
visualize_circuit(q1)
measure = q1.measure()
visualize_measurement(measure)