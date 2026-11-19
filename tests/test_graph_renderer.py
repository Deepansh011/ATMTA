import json
from pathlib import Path

from core.converter import convert_mealy_to_moore
from core.io import example_to_machine
from visualization.graph_renderer import mealy_svg, moore_svg


def test_svg_exports_render_for_a_converted_machine():
    example = json.loads(
        (Path(__file__).parents[1] / "examples" / "sample_machines.json").read_text()
    )[0]
    mealy = example_to_machine(example)
    moore, _ = convert_mealy_to_moore(mealy)

    assert mealy_svg(mealy).endswith("</svg>")
    assert moore_svg(moore).endswith("</svg>")
