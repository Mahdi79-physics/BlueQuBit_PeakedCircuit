# ⚡ BlueQuBit Hackathon – Peaked Circuit Sampling

This repository contains the **44-qubit peaked circuit sampling project** for the BlueQuBit Hackathon.  
It demonstrates **splitting large circuits, running on IBM Quantum backends, and analyzing peak bitstrings**.

---

## 🧠 Features

- ⚡ Split large 44-qubit circuits into **smaller subcircuits** for execution  
- 🔗 Reconstruct **peak candidates** from subcircuits  
- 🎯 Use **IBM Quantum SamplerV2** for high-shot sampling  
- 📊 Plot **normalized frequencies** of top bitstrings  
- 🖥️ Compatible with **AerSimulator** for local testing  
- 🔄 Transpile circuits with **optimization levels** for hardware  

---

## 📝 Requirements

- Python 3.8+  
- Qiskit  
- Qiskit IBM Runtime (`qiskit-ibm-runtime`)  
- NumPy  
- Matplotlib  

Install dependencies:

```bash
pip install -r requirements.txt
