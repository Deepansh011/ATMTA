import pandas as pd
import streamlit as st

from core.converter import convert_mealy_to_moore
from core.models import MealyMachine
from core.simulator import simulate_mealy, simulate_moore
from core.validator import validate_mealy


st.set_page_config(page_title="Mealy to Moore Converter", page_icon="M", layout="wide")
st.markdown(
    """<style>
    html, body, [class*="css"] {font-family: Arial, Helvetica, sans-serif;}
    .stApp {background: #ffffff; color: #1f2937;}
    .block-container {max-width: 1100px; padding-top: 2rem;}
    h1 {color: #1e3a8a;}
    </style>""",
    unsafe_allow_html=True,
)


def default_rows():
    return pd.DataFrame(
        [
            {"State": "A", "Input": "0", "Next state": "A", "Output": "0"},
            {"State": "A", "Input": "1", "Next state": "B", "Output": "1"},
            {"State": "B", "Input": "0", "Next state": "B", "Output": "1"},
            {"State": "B", "Input": "1", "Next state": "A", "Output": "0"},
        ]
    )


def make_machine(states_text, inputs_text, outputs_text, initial, rows):
    states = tuple(x.strip() for x in states_text.split(",") if x.strip())
    inputs = tuple(x.strip() for x in inputs_text.split(",") if x.strip())
    outputs = tuple(x.strip() for x in outputs_text.split(",") if x.strip())
    transitions = {}

    for _, row in rows.iterrows():
        if any(pd.isna(row[column]) for column in ["State", "Input", "Next state", "Output"]):
            continue
        key = (str(row["State"]).strip(), str(row["Input"]).strip())
        if key in transitions:
            raise ValueError(f"Duplicate transition for state {key[0]!r} on input {key[1]!r}.")
        transitions[key] = (str(row["Next state"]).strip(), str(row["Output"]).strip())

    return MealyMachine(states, inputs, outputs, initial, transitions)


if "table" not in st.session_state:
    st.session_state.table = default_rows()
if "result" not in st.session_state:
    st.session_state.result = None

st.title("Mealy to Moore Converter")
st.write("Enter a complete Mealy machine transition table, then click **Convert to Moore Machine**.")

with st.expander("How to use", expanded=True):
    st.markdown(
        """
        1. Enter comma-separated state names, input symbols, and output symbols.
        2. Choose the initial state.
        3. Fill one transition row for every state and input combination.
        4. Click **Convert to Moore Machine**.

        Example: for states `A, B` and inputs `0, 1`, the table needs four rows: A/0, A/1, B/0, and B/1.
        """
    )

left, right = st.columns(2)
with left:
    states_text = st.text_input("States", "A, B")
    inputs_text = st.text_input("Input alphabet", "0, 1")
with right:
    outputs_text = st.text_input("Output alphabet", "0, 1")
    state_options = tuple(x.strip() for x in states_text.split(",") if x.strip()) or ("A",)
    initial_state = st.selectbox("Initial state", state_options)

st.subheader("Mealy transition table")
edited_rows = st.data_editor(
    st.session_state.table,
    num_rows="dynamic",
    use_container_width=True,
    key="transition_table",
)

if st.button("Convert to Moore Machine", type="primary"):
    try:
        machine = make_machine(
            states_text, inputs_text, outputs_text, initial_state, edited_rows
        )
        errors = validate_mealy(machine)
        if errors:
            st.session_state.result = None
            st.error("Please correct the Mealy machine before converting.")
            for error in errors:
                st.write(f"• {error}")
        else:
            converted, _ = convert_mealy_to_moore(machine)
            st.session_state.result = (machine, converted)
    except ValueError as error:
        st.session_state.result = None
        st.error(str(error))

if st.session_state.result:
    machine, moore = st.session_state.result
    st.success("Conversion completed.")
    st.subheader("Moore states and outputs")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Moore state": state.name,
                    "Original Mealy state": state.origin or "Initial state",
                    "State output": state.output,
                }
                for state in moore.states
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Moore transition table")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "State": state.name,
                    "Input": symbol,
                    "Next state": moore.transitions[(state.name, symbol)],
                }
                for state in moore.states
                for symbol in moore.inputs
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.info(
        "The Moore machine begins at START with output ε (initial). "
        "For comparison with the Mealy machine, ignore this first Moore output."
    )

    st.subheader("Simulator")
    st.write("Enter an input string and compare the outputs of both machines.")
    input_word = st.text_input("Input string", "0101")
    if st.button("Run Simulation"):
        try:
            if any(len(symbol) > 1 for symbol in moore.inputs):
                symbols = input_word.split()
            else:
                symbols = list(input_word)

            _, mealy_output, mealy_rows = simulate_mealy(machine, symbols)
            _, moore_outputs, moore_rows = simulate_moore(moore, symbols)
            aligned_moore_output = "".join(moore_outputs[1:])

            st.success(
                "Outputs match." if mealy_output == aligned_moore_output else "Outputs do not match."
            )
            st.write(f"Mealy output: `{mealy_output}`")
            st.write(f"Moore output after START: `{aligned_moore_output}`")
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Step": 0,
                            "Input": "-",
                            "Mealy state": machine.initial,
                            "Mealy output": "-",
                            "Moore state": moore.initial,
                            "Moore output": moore_outputs[0],
                        },
                        *[
                            {
                                "Step": index + 1,
                                "Input": symbol,
                                "Mealy state": mealy_rows[index][4],
                                "Mealy output": mealy_rows[index][3],
                                "Moore state": moore_rows[index][4],
                                "Moore output": moore_outputs[index + 1],
                            }
                            for index, symbol in enumerate(symbols)
                        ],
                    ]
                ),
                use_container_width=True,
                hide_index=True,
            )
        except ValueError as error:
            st.error(str(error))
