from collections import defaultdict, deque
from .models import MealyMachine, MooreMachine, MooreState

EPSILON = 'ε (initial)'

def convert_mealy_to_moore(m: MealyMachine, prune_unreachable=True):
    incoming=defaultdict(set)
    for (q,a),(p,o) in m.transitions.items(): incoming[p].add(o)
    variants={}
    used_names=set()
    for q in m.states:
        for o in sorted(incoming[q]):
            base=f'{q} / {o}'; name=base; suffix=2
            while name in used_names:
                name=f'{base} #{suffix}'; suffix+=1
            variants[(q,o)]=name; used_names.add(name)
    initial='START'
    # Avoid collisions with user-defined labels.
    while initial in variants.values(): initial += "'"
    states=[MooreState(initial,None,EPSILON,True)] + [MooreState(n,q,o) for (q,o),n in variants.items()]
    trans={}
    for a in m.inputs:
        p,o=m.transitions[(m.initial,a)]; trans[(initial,a)]=variants[(p,o)]
    for (q,prev),name in variants.items():
        for a in m.inputs:
            p,o=m.transitions[(q,a)]
            trans[(name,a)]=variants[(p,o)]
    if prune_unreachable:
        reachable={initial}; todo=deque([initial])
        while todo:
            q=todo.popleft()
            for a in m.inputs:
                p=trans[(q,a)]
                if p not in reachable: reachable.add(p); todo.append(p)
        states=[s for s in states if s.name in reachable]
        trans={k:v for k,v in trans.items() if k[0] in reachable}
    trace=[
      {'title':'STEP 1 · Read the Mealy table','math':'The machine is M = (Q, Σ, Γ, δ, λ, q₀). Each defined cell supplies one destination and one output.','result':f'{len(m.states)} states, {len(m.inputs)} inputs, {len(m.transitions)} transitions.'},
      {'title':'STEP 2 · Collect incoming outputs','math':'For each destination p, collect I(p) = {λ(q,a) | δ(q,a)=p}.','result':'; '.join(f'{q}: {{{", ".join(sorted(incoming[q])) or "∅"}}}' for q in m.states)},
      {'title':'STEP 3 · Group destination states','math':'Each distinct incoming output induces a Moore variant (p,o).','result':'; '.join(f'{q} → {{{", ".join(sorted(incoming[q])) or "∅"}}}' for q in m.states)},
      {'title':'STEP 4 · Explain state splitting','math':'A destination must split exactly when it can be entered with different outputs, because Moore output belongs to the destination state.','result':'; '.join(f'{q}: {len(incoming[q])} variant(s)' for q in m.states)},
      {'title':'STEP 5 · Generate variants','math':'Create one state (p,o) for every observed incoming output o.','result':'; '.join(f'{n} = output {o}' for (q,o),n in variants.items()) or 'No variants; initial state handles all behavior.'},
      {'title':'STEP 6 · Generate transitions','math':'From (q,prev), on a, go to (δ(q,a), λ(q,a)); the destination state carries the emitted output.','result':f"{len(trans)} transition(s) generated; the initial state's outgoing edges use the same rule."},
      {'title':'STEP 7 · Create initial state','math':'The Mealy machine emits nothing before input. The Moore start state therefore uses the explicit sentinel ε (initial), then emits one output after each symbol.','result':f'Initial state: {initial}, output: {EPSILON}.'},
      {'title':'STEP 8 · Remove unreachable variants','math':'Breadth-first reachability starts at the dedicated initial state.','result':f'{len(states)} reachable Moore states retained (pruning={prune_unreachable}).'},
      {'title':'STEP 9 · Final Moore machine','math':'M′ has the same input alphabet; λ′ is the output stored on each state. Drop only the start sentinel when comparing consumed-symbol outputs.','result':f'{len(states)} states, {len(trans)} transitions.'},
    ]
    return MooreMachine(tuple(states),m.inputs,m.outputs,initial,trans,EPSILON,m.initial),trace
