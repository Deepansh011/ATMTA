# Mealy to Moore Machine Converter

An interactive Automata Theory project that converts a complete deterministic Mealy machine into an equivalent Moore machine using the standard state-splitting construction.

**Live application:** [deepansh.streamlit.app](https://deepansh.streamlit.app/)

## Project objective

The project demonstrates how output labels on Mealy transitions can be moved to Moore states without changing the output produced for an input string. It is designed for classroom demonstration: the user enters a Mealy transition table, converts it, views both state diagrams, and simulates the two machines.

## Features

- Create a complete deterministic Mealy machine from a transition table.
- Validate states, input symbols, output symbols, initial state, duplicate transitions, and missing transitions.
- Convert the machine using incoming-output state splitting.
- Show the generated Moore states, their outputs, and the Moore transition table.
- Display 2D diagrams for both machines.
  - Mealy diagram: edge labels are `input/output`.
  - Moore diagram: each state contains its output; edge labels are inputs.
- Simulate an input string on both machines and compare the output sequences step by step.
- Support self-loops, multiple output symbols, one-state machines, and destination-state splitting.

## Formal model

A Mealy machine is represented by:

`M = (Q, Σ, Γ, δ, λ, q₀)`

where `δ(q, a)` gives the next state and `λ(q, a)` gives the output produced on a transition.

A Moore machine is represented by:

`M′ = (Q′, Σ, Γ, δ′, λ′, q′₀)`

where each state has one fixed output `λ′(q′)`.

## Conversion method

For every Mealy transition

`q --a/o--> p`

the converter creates or uses the Moore state `(p, o)`. The output `o` is stored on that destination state. Therefore, if the same Mealy destination state is entered with different outputs, it is split into separate Moore states.

The Moore transition is:

`(q, previous_output) --a--> (δ(q, a), λ(q, a))`

The converter also creates a dedicated `START` Moore state with the output `ε (initial)`.

### Output alignment

A Mealy machine produces one output for each input symbol. A Moore machine produces an initial state output and then one output after each input symbol. To compare the two machines, the application ignores the initial `ε (initial)` output of the Moore machine.

## How to use the web application

1. Open [deepansh.streamlit.app](https://deepansh.streamlit.app/).
2. Enter the states, input alphabet, output alphabet, and initial state.
3. Fill the Mealy transition table. Each state/input pair requires exactly one row.
4. Click **Convert to Moore Machine**.
5. Inspect the generated Moore table and the two state diagrams.
6. Enter an input string and click **Run Simulation** to compare outputs.

The included default example is a valid binary machine. Click **Convert to Moore Machine** immediately to see a working conversion.

## Example of state splitting

If a Mealy state `B` is reached with both output `0` and output `1`, one Moore state cannot represent both outputs. The construction creates:

| Moore state | Meaning | State output |
| --- | --- | --- |
| `B / 0` | Entered Mealy state `B` after an output of `0` | `0` |
| `B / 1` | Entered Mealy state `B` after an output of `1` | `1` |

This is the central idea that preserves the Mealy machine's output behaviour.

## Testing

The project includes automated tests for validation, conversion, simulation, import/export helpers, SVG diagram generation, self-loops, state splitting, unreachable states, and output alignment.

An additional deterministic test generates **50 different complete Mealy machines** with varied state counts, input alphabets, output alphabets, loops, and splits. For each machine, the tests verify:

- the Mealy machine is valid;
- the construction-based equivalence verifier succeeds;
- the Mealy and aligned Moore output sequences agree for all input words up to length 3;
- both diagram generators contain the expected states and transitions.

Run all tests locally:

```bash
python -m pytest -q
```

## Run locally

```bash
git clone https://github.com/Deepansh011/ATMTA.git
cd ATMTA
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Then open `http://localhost:8501` in a browser.

## Technology used

- Python 3.11+
- Streamlit
- Pandas
- Graphviz-compatible DOT diagrams
- Pytest

## Project structure

```text
ATMTA/
├── app.py                 # Streamlit interface
├── core/                  # Models, validation, conversion, simulation, verification
├── visualization/         # Mealy and Moore diagram generators
├── tests/                 # Automated tests, including 50 generated machines
├── examples/              # Sample machine definitions
├── docs/                  # Theory, algorithm notes, and project report
├── requirements.txt
└── runtime.txt
```

## References

- Michael Sipser, *Introduction to the Theory of Computation*, 3rd edition, Cengage Learning, 2012.
- John E. Hopcroft, Rajeev Motwani, and Jeffrey D. Ullman, *Introduction to Automata Theory, Languages, and Computation*, 3rd edition, Pearson, 2006.
