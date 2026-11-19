import json
from pathlib import Path
import pytest
from core.io import example_to_machine
from core.converter import convert_mealy_to_moore
from core.validator import validate_mealy
from core.verifier import verify

EX=json.loads((Path(__file__).parents[1]/'examples/sample_machines.json').read_text())
def test_examples_convert_and_verify():
    for obj in EX:
        m=example_to_machine(obj); mo,tr=convert_mealy_to_moore(m)
        assert validate_mealy(m)==[] and tr[-1]['title'].startswith('STEP 9')
        assert verify(m,mo)['valid']
def test_splitting_different_incoming_outputs():
    mo,_=convert_mealy_to_moore(example_to_machine(EX[1]))
    variants=[s for s in mo.states if s.origin=='t']
    assert {s.output for s in variants}=={'x','y'}
def test_single_state_loop_and_initial():
    from core.models import MealyMachine
    m=MealyMachine(('q',),('0',),('x','y'),'q',{('q','0'):('q','y')})
    mo,_=convert_mealy_to_moore(m)
    assert len(mo.states)==2 and mo.states[0].initial
    assert mo.transitions[(mo.initial,'0')]=='q / y'
    assert mo.transitions[('q / y','0')]=='q / y'
def test_unreachable_states_pruned():
    from core.models import MealyMachine
    m=MealyMachine(('a','b','z'),('0',),('x',),'a',{('a','0'):('b','x'),('b','0'):('b','x'),('z','0'):('z','x')})
    mo,_=convert_mealy_to_moore(m)
    assert all(s.origin!='z' for s in mo.states)
def test_conversion_preserves_all_words_bounded():
    from itertools import product
    from core.simulator import simulate_mealy,simulate_moore
    for obj in EX:
        m=example_to_machine(obj); mo,_=convert_mealy_to_moore(m)
        for n in range(5):
            for w in product(m.inputs,repeat=n):
                assert simulate_mealy(m,w)[1]==''.join(simulate_moore(mo,w)[1][1:])
