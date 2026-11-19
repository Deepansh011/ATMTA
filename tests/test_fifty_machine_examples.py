from itertools import product
from random import Random

from core.converter import convert_mealy_to_moore
from core.models import MealyMachine
from core.simulator import simulate_mealy, simulate_moore
from core.validator import validate_mealy
from core.verifier import verify
from visualization.graph_renderer import dot_mealy, dot_moore, mealy_svg, moore_svg


def generated_machines(count=50):
    """Create deterministic complete examples with loops, splits, and varied alphabets."""
    random = Random(20261119)
    for number in range(count):
        state_count = 1 + number % 5
        input_count = 1 + number % 3
        output_count = 2 + number % 3
        states = tuple(f"q{index}" for index in range(state_count))
        inputs = tuple(str(index) for index in range(input_count))
        outputs = tuple(str(index) for index in range(output_count))
        transitions = {
            (state, symbol): (random.choice(states), random.choice(outputs))
            for state in states
            for symbol in inputs
        }
        yield MealyMachine(states, inputs, outputs, states[0], transitions)


def test_fifty_examples_preserve_outputs_and_generate_correct_diagram_data():
    for machine in generated_machines():
        assert validate_mealy(machine) == []
        moore, _ = convert_mealy_to_moore(machine)
        assert verify(machine, moore)["valid"]

        for length in range(4):
            for word in product(machine.inputs, repeat=length):
                assert simulate_mealy(machine, word)[1] == "".join(
                    simulate_moore(moore, word)[1][1:]
                )

        mealy_dot = dot_mealy(machine)
        moore_dot = dot_moore(moore)
        assert mealy_dot.startswith("digraph G {") and mealy_dot.endswith("}")
        assert moore_dot.startswith("digraph G {") and moore_dot.endswith("}")
        assert mealy_dot.count(" [label=") >= len(machine.transitions)
        assert moore_dot.count(" [label=") >= len(moore.transitions)

        mealy_image = mealy_svg(machine)
        moore_image = moore_svg(moore)
        assert mealy_image.count("<circle") == len(machine.states)
        assert moore_image.count("<circle") == len(moore.states)
        assert mealy_image.endswith("</svg>")
        assert moore_image.endswith("</svg>")
