# Simulador de Autómatas Finitos (AFD / AFND)

This is a desktop application developed in the PYTHON programming language using the Tkinter library. The program allows analyzing, converting and simulating Deterministic and Non-Deterministic Finite Automata (DFA / NFA) through an interactive graphical interface.

## MAIN FEATURES

**Automata Definition and Visualization**  
INCLUDES:
* Import of `.json` files generated from JFLAP.
* Extraction of the automaton formal definition:  
  \( Q, \Sigma, q_0, F, \delta \)
* Visualization of the transition function in an interactive table.
* Event console showing automaton information.

**Simulation and String Validation**
* Evaluation of input strings.
* Step-by-step state transition trace.
* Final result showing if the string is **Accepted** or **Rejected**.

**Extra Tools**
* Calculation of prefixes, suffixes and substrings (including **λ**).
* Generation of **Kleene Closure (Σ\*)**.
* Generation of **Positive Closure (Σ+)** with user-defined maximum length.

**File Converter**
* Converts JFLAP `.jff` files into `.json` and `.xml`.
* Ignores corrupted or empty files automatically.

## REQUIREMENTS

* Python 3.8 or higher.
* Tkinter library (included with Python).
* JFLAP files (`.jff`) for automata conversion.

## Installation and Execution

Follow these steps to run the program on your local machine:

1. **Open your terminal** and navigate to the project folder.
2. **Convert JFLAP files** (if needed):
   ```bash
   python convertidor.py
   ```
3. **Run the simulator**
   ```bash
   python main.py
   ```