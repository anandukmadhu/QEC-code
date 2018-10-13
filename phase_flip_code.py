#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 11:46:45 2018

@author: anandu
"""

import sys
try:
    sys.path.append("../../") 
    import Qconfig
    qx_config = {
        "APItoken": Qconfig.APItoken,
        "url": Qconfig.config['url']}
except:
    qx_config = {
        "APItoken":"*****",
        "url":"https://quantumexperience.ng.bluemix.net/api"}
    
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import QuantumProgram

from qiskit.tools.visualization import plot_histogram

from IBMQuantumExperience import IBMQuantumExperience
api = IBMQuantumExperience(token=qx_config['APItoken'], config={'url': qx_config['url']})

from qiskit.backends import discover_remote_backends
backends = discover_remote_backends(api)

backend = 'local_qasm_simulator' 
shots = 1024  

Q_program = QuantumProgram()

q3 = QuantumRegister('q3', 3)
c3 = ClassicalRegister('c3', 3)

p_flip=QuantumCircuit(q3,c3)

p_flip.h(q3[0])
p_flip.cx(q3[0],q3[1])
p_flip.cx(q3[0],q3[2])

p_flip.h(q3[0])
p_flip.h(q3[1])
p_flip.h(q3[2])

p_flip.iden(q3[0])
p_flip.iden(q3[1])
p_flip.iden(q3[2])

p_flip.z(q3[0])


p_flip.h(q3[0])
p_flip.h(q3[1])
p_flip.h(q3[2])

p_flip.cx(q3[0],q3[2])
p_flip.cx(q3[0],q3[1])
p_flip.ccx(q3[2],q3[1],q3[0])

measureZ=QuantumCircuit(q3,c3)

measureZ.measure(q3[2],c3[2])
measureZ.measure(q3[1],c3[1])
measureZ.measure(q3[0],c3[0])

Q_program.add_circuit("p_flip_code",p_flip+measureZ)
circuits = ["p_flip_code"]
result = Q_program.execute(circuits, backend=backend, shots=shots, max_credits=3, wait=10, timeout=600)
plot_histogram(result.get_counts("p_flip_code"))
print(result.get_counts("p_flip_code"))

