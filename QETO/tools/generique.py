import random
import numpy as np
from QETO.gate.gate import NATIVE_GATE, ControlGate, ParameterGate, U
from QETO.quantum_circuit import QCircuit


def random_circuit(
    gate_classes: list[type]= NATIVE_GATE, nb_qubits: int= 5, nb_gates: int = np.random.randint(5, 10)
):

    qubits = list(range(nb_qubits))
    qcircuit = QCircuit(nb_qubits)
    if any(
        issubclass(gate, ControlGate)  and nb_qubits <= 1
        for gate in gate_classes
    ):
        raise ValueError("number of qubits to low for this gates")

    for _ in range(nb_gates):
        gate_class = random.choice(gate_classes)
        target = random.choice(qubits)
        if not issubclass(gate_class, ControlGate):
            if issubclass(gate_class, ParameterGate):
                if gate_class == U:  # type: ignore[reportUnnecessaryComparison]
                    theta = float(random.uniform(0, 2 * np.pi))
                    phi = float(random.uniform(0, 2 * np.pi))
                    gamma = float(random.uniform(0, 2 * np.pi))
                    qcircuit.add(U(target, theta, phi, gamma))
                else:
                    qcircuit.add(gate_class(target, float(random.uniform(0, 2 * np.pi))))  # type: ignore[reportCallIssue]
            else:
                qcircuit.add(gate_class(target))
        else:
            control = random.choice(qubits)
            while control == target:
                control = random.choice(qubits)
            if issubclass(gate_class, ParameterGate):
                qcircuit.add(gate_class(control, target, float(random.uniform(0, 2 * np.pi))))  # type: ignore[reportArgumentType]
            else:
                qcircuit.add(gate_class(control, target))
    return qcircuit