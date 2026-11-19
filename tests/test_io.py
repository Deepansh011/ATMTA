from core.models import MealyMachine
from core.io import machine_to_json,machine_from_json,mealy_csv,example_to_machine
import json
from pathlib import Path

def test_json_roundtrip_and_csv():
    obj=json.loads((Path(__file__).parents[1]/'examples/sample_machines.json').read_text())[0]
    m=example_to_machine(obj); restored=machine_from_json(machine_to_json(m))
    assert restored==m and 'State,Input,Next state,Output' in mealy_csv(m)
def test_duplicate_json_transitions_rejected():
    import pytest
    with pytest.raises(ValueError): machine_from_json('{"states":["q"],"inputs":["0"],"outputs":["x"],"initial":"q","transitions":[{"source":"q","input":"0","destination":"q","output":"x"},{"source":"q","input":"0","destination":"q","output":"x"}]}')
