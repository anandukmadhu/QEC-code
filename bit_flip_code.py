#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 14:57:01 2018

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

backend = 'ibmqx4' 
shots = 1024  

Q_program = QuantumProgram()

q3 = QuantumRegister('q3', 3)
c3 = ClassicalRegister('c3', 3)

b_flip=QuantumCircuit(q3,c3)

b_flip.h(q3[0])
b_flip.cx(q3[0],q3[1])
b_flip.cx(q3[0],q3[2])

b_flip.iden(q3[0])
b_flip.iden(q3[1])
b_flip.iden(q3[2])

b_flip.x(q3[0])

b_flip.cx(q3[0],q3[2])
b_flip.cx(q3[0],q3[1])
b_flip.ccx(q3[2],q3[1],q3[0])

measureZ=QuantumCircuit(q3,c3)

measureZ.measure(q3[2],c3[2])
measureZ.measure(q3[1],c3[1])
measureZ.measure(q3[0],c3[0])

Q_program.add_circuit("b_flip_code",b_flip+measureZ)
circuits = ["b_flip_code"]
result = Q_program.execute(circuits, backend=backend, shots=shots, max_credits=3, wait=10, timeout=600)
plot_histogram(result.get_counts("b_flip_code"))
print(result.get_counts("b_flip_code"))
