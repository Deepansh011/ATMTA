import json
from pathlib import Path
import pytest
from core.io import example_to_machine
from core.converter import convert_mealy_to_moore
from core.simulator import simulate_mealy,simulate_moore
EX=json.loads((Path(__file__).parents[1]/'examples/sample_machines.json').read_text())
def test_output_alignment_and_history():
    m=example_to_machine(EX[0]); mo,_=convert_mealy_to_moore(m)
    _,a,rows=simulate_mealy(m,'0101'); _,b,mrows=simulate_moore(mo,'0101')
    assert a==''.join(b[1:]); assert len(rows)==len(mrows)==4; assert len(b)==5
def test_invalid_input_rejected():
    m=example_to_machine(EX[0])
    with pytest.raises(ValueError): simulate_mealy(m,'2')
