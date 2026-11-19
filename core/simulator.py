def simulate_mealy(machine, word):
    q=machine.initial; rows=[]; out=[]
    for i,a in enumerate(word,1):
        if a not in machine.inputs: raise ValueError(f'Invalid input symbol {a!r} at position {i}.')
        dest,o=machine.transitions[(q,a)]; rows.append((i,a,q,o,dest)); q=dest; out.append(o)
    return q,''.join(out),rows

def simulate_moore(machine, word):
    q=machine.initial; outputs=[machine.state_map[q].output]; rows=[]
    for i,a in enumerate(word,1):
        if a not in machine.inputs: raise ValueError(f'Invalid input symbol {a!r} at position {i}.')
        dest=machine.transitions[(q,a)]; o=machine.state_map[dest].output
        rows.append((i,a,q,o,dest)); q=dest; outputs.append(o)
    return q,outputs,rows
