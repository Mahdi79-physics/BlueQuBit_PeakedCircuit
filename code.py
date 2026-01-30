from qiskit import qasm, qasm2,qasm3
from qiskit.circuit import QuantumCircuit, ClassicalRegister, Gate, library
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, Batch, SamplerV2 as Sampler

import numpy as np
from matplotlib import pyplot as plt

from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(
    channel='ibm_quantum',
    instance='ibm-q/open/main',
    token='d786b5d89b9478db9ef40cf3a486a89dd64a3aa9019141a60bfcd138f11332aa92ba8e31aa9cb589e085c9e672e8ba6a3e6e252b1d8fa9ce7309d94899575b0c'
)

# Or save your credentials on disk.
# QiskitRuntimeService.save_account(channel='ibm_quantum', instance='ibm-q/open/main', token='d786b5d89b9478db9ef40cf3a486a89dd64a3aa9019141a60bfcd138f11332aa92ba8e31aa9cb589e085c9e672e8ba6a3e6e252b1d8fa9ce7309d94899575b0c')



# Print all available backends you can use
for backend in service.backends():
    print(backend.name)


backend = service.backend("ibm_kyiv")


from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

def extract_subcircuit(qc, qubit_indices):
    sub_qreg = QuantumRegister(len(qubit_indices), 'q')
    sub_creg = ClassicalRegister(len(qubit_indices), 'c')
    sub_circ = QuantumCircuit(sub_qreg, sub_creg)

    #mapping to subcircuits
    qubit_map = {qc.qubits[i]: sub_qreg[j] for j, i in enumerate(qubit_indices)}

    for instr in qc.data:
        qargs = instr.qubits
        cargs = instr.clbits

        if all(q in qubit_map for q in qargs):
            new_qargs = [qubit_map[q] for q in qargs]
            sub_circ.append(instr.operation, new_qargs, cargs)

    return sub_circ



qc_full = QuantumCircuit.from_qasm_file("/content/P5_granite_summit (1).qasm")

qc1 = extract_subcircuit(qc_full, list(range(27)))
qc1.measure_all()

qc2 = extract_subcircuit(qc_full, list(range(27, 44)))
qc2.measure_all()



sampler = Sampler(backend, options={"default_shots": 1000})

qc1 = extract_subcircuit(qc_full, list(range(27)))
qc1.measure_all()

qc2 = extract_subcircuit(qc_full, list(range(27, 44)))
qc2.measure_all()


pm1 = generate_preset_pass_manager(3, backend=backend)
tp1 = pm1.run(qc1)

pm2 = generate_preset_pass_manager(3, backend=backend)
tp2 = pm2.run(qc2)


!pip uninstall qiskit -y
!pip install qiskit qiskit-aer --upgrade --quiet

from qiskit import transpile
from qiskit_aer import AerSimulator

# Use AerSimulator backend
sim = AerSimulator()

# Transpile and run first half (qubits 0–26)
tp1 = transpile(qc1, backend=sim)
result1 = sim.run(tp1, shots=1000).result()
counts1 = result1.get_counts()

# Transpile and run second half (qubits 27–43)
tp2 = transpile(qc2, backend=sim)
result2 = sim.run(tp2, shots=1000).result()
counts2 = result2.get_counts()

# Peak detection
peak1 = max(counts1, key=counts1.get)
peak2 = max(counts2, key=counts2.get)
print(f"Peak 0–26: {peak1}")
print(f"Peak 27–43: {peak2}")
print(f" Combined peak (44 qubits): {peak2 + peak1}")



def plot_counts(counts, title, top_n=10):
    sorted_cts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
    bitstrings = list(sorted_cts.keys())[:top_n]
    frequencies = np.array(list(sorted_cts.values())[:top_n])
    total = sum(counts.values())

    plt.figure(figsize=(10, 4))
    plt.bar(bitstrings, frequencies / total, color='steelblue')
    plt.title(title)
    plt.xlabel("Bitstring")
    plt.ylabel("Normalized Frequency")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()


plot_counts(counts1, "Top 10 Bitstrings for Qubits 0–26")
result1 = job1.result()
counts1 = result1[0].data.meas.get_counts()

result2 = job2.result()
counts2 = result2[0].data.meas.get_counts()

peak1 = max(counts1, key=counts1.get)
peak2 = max(counts2, key=counts2.get)

print(f"Peak (0–26): {peak1}")
print(f"Peak (27–43): {peak2}")
print(f"🔗 Combined Peak (44 qubits): {peak2 + peak1}")


# 🧠 Peak bitstring for first half (qubits 0–26)
peak1 = max(counts1, key=counts1.get)
print(f"Peak in qubits 0–26: {peak1} ({counts1[peak1]} counts)")

# 🧠 Peak bitstring for second half (qubits 27–43)
peak2 = max(counts2, key=counts2.get)
print(f"Peak in qubits 27–43: {peak2} ({counts2[peak2]} counts)")

# 🧬 Optional: Stitch to get 44-bit full peak candidate
combined_peak = peak2 + peak1
print(f"\n🔗 Reconstructed 44-qubit peak (approx): {combined_peak}")


## Load the circuit you would like to run
circuit = QuantumCircuit.from_qasm_file('/content/P5_granite_summit (1).qasm')

## In case qasm instructions do not contain measurement instructions, we can add them here
circuit.measure_all()
print(circuit.count_ops())


## We have to transpile the circuits to a physical device, device connectivy, basis gate set etc.
## For more details see: https://docs.quantum.ibm.com/api/qiskit/transpiler
optimization_level = 3
pm = generate_preset_pass_manager(optimization_level,
                                  backend=backend)

tp_circuit = pm.run(circuit)

print(tp_circuit.count_ops())
# tp_circuit.draw('mpl', fold=-1, idle_wires=False)


sampler = Sampler(backend, options={"default_shots": 100000})

## In sampler we run pubs, which is a collection/list of circuits or tuples of circuits and parameters: https://docs.quantum.ibm.com/api/qiskit/qiskit.primitives.BackendSamplerV2
job = sampler.run([tp_circuit])
print(job.job_id())


## we can either retrieved the data directly from the job, or if we have the job_id, we can retrieve it with:
job = service.job('czxaw9hqnmvg008vzc0g')
counts = job.result()[0].data.meas.get_counts()

## we sort the count dictionary from highest count to lowest
sorted_cts_dict={k: v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}


cutoff = 50 #how many bitstrings we want to plot
val_list = list(sorted_cts_dict.values())
string_list = list(sorted_cts_dict.keys())
plt.bar(range(cutoff), np.array(val_list)[0:cutoff]/sum(val_list), label = f"Peak: {string_list[0]}")
plt.ylabel('Frequency')
plt.xlabel('Bit-string index')
plt.legend()
plt.show()


