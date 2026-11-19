from collections import deque
from .validator import validate_mealy

def verify(mealy, moore):
    errors=validate_mealy(mealy); checked=0; correspondences=set(); issues=[]
    if errors: return {'valid':False,'issues':errors,'transitions_checked':0,'correspondences_checked':0}
    sm=moore.state_map
    if moore.initial not in sm or not sm[moore.initial].initial: issues.append('Dedicated initial Moore state is missing.')
    todo=deque([(mealy.initial,moore.initial)]); seen=set()
    while todo:
        q,r=todo.popleft()
        if (q,r) in seen: continue
        seen.add((q,r)); ms=sm.get(r)
        if ms is None: issues.append(f'Unknown Moore state {r}.'); continue
        if ms.origin is not None and ms.origin != q: issues.append(f'Origin mismatch for {r}: expected {q}.')
        correspondences.add((q,r))
        for a in mealy.inputs:
            p,o=mealy.transitions[(q,a)]; rp=moore.transitions.get((r,a)); checked+=1
            if rp is None or rp not in sm: issues.append(f'Missing Moore transition from {r} on {a}.'); continue
            ds=sm[rp]
            if ds.origin != p or ds.output != o: issues.append(f'Correspondence mismatch for {q} --{a}/{o}--> {p}.')
            todo.append((p,rp))
    return {'valid':not issues,'issues':issues,'transitions_checked':checked,'correspondences_checked':len(correspondences),'explanation':'Every reachable Mealy step maps to a Moore edge whose destination carries that step’s Mealy output. Thus output strings agree after removing the initial sentinel.'}
