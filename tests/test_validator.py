from core.models import MealyMachine
from core.validator import validate_mealy

def test_missing_transition():
    m=MealyMachine(('q',),('0','1'),('x',),'q',{('q','0'):('q','x')})
    assert any('Missing transition' in x for x in validate_mealy(m))
def test_undefined_output_and_initial():
    m=MealyMachine(('q',),('0',),('x',),'z',{('q','0'):('q','bad')})
    e=validate_mealy(m); assert any('initial' in x.lower() for x in e); assert any('outside' in x for x in e)
def test_duplicate_alphabet():
    m=MealyMachine(('q','q'),('0',),('x',),'q',{('q','0'):('q','x')})
    assert any('unique' in x for x in validate_mealy(m))
