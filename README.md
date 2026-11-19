# Mealy–Moore Machine Transformation Studio

A Streamlit application for authoring deterministic Mealy machines, converting them with incoming-output state splitting, inspecting a generated trace, simulating input words, and checking the construction.

## Install and launch (macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Run the automated suite with `python -m pytest -q`.

## Put it online with Streamlit Community Cloud

1. Create a new GitHub repository and upload the contents of this folder.
2. Open [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Select **Create app**.
4. Choose your repository, branch, and the file `app.py`.
5. Click **Deploy**.

The hosting service reads `requirements.txt` to install the packages and `runtime.txt` to use Python 3.11. It will give you a public website link after deployment.

## Mathematical convention

A Mealy run emits one symbol per consumed input. A Moore run emits its current state's output before input and after every transition. The generated initial state uses the sentinel `ε (initial)`; equivalence compares the Mealy outputs with the Moore outputs after removing that initial sentinel.

## Project layout

- `core/`: formal machine models, validation, conversion, simulation, verification, and serialization.
- `visualization/`: Graphviz diagrams and deterministic standalone SVG export.
- `examples/`: four complete sample machines.
- `tests/`: conversion, validation, simulation, and import/export tests.
- `docs/`: project report and algorithm notes.
