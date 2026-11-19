from .models import MealyMachine

def validate_mealy(m: MealyMachine) -> list[str]:
    e=[]
    if not m.states: e.append('At least one state is required.')
    if not m.inputs: e.append('At least one input symbol is required.')
    if not m.outputs: e.append('At least one output symbol is required.')
    if len(set(m.states)) != len(m.states): e.append('State names must be unique.')
    if len(set(m.inputs)) != len(m.inputs): e.append('Input symbols must be unique.')
    if len(set(m.outputs)) != len(m.outputs): e.append('Output symbols must be unique.')
    if m.initial not in m.states: e.append(f'Initial state {m.initial!r} is undefined.')
    expected={(q,a) for q in m.states for a in m.inputs}
    for key,(dest,out) in m.transitions.items():
        q,a=key
        if q not in m.states: e.append(f'Transition source {q!r} is undefined.')
        if a not in m.inputs: e.append(f'Input {a!r} is outside the input alphabet.')
        if dest not in m.states: e.append(f'Transition destination {dest!r} is undefined.')
        if out not in m.outputs: e.append(f'Output {out!r} is outside the output alphabet.')
    for q,a in sorted(expected-set(m.transitions)): e.append(f'Missing transition for ({q}, {a}).')
    for q,a in sorted(set(m.transitions)-expected): e.append(f'Unexpected/duplicate transition for ({q}, {a}).')
    return e
