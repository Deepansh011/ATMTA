import json
import pandas as pd
from .models import MealyMachine

def example_to_machine(obj):
    t={tuple(k.split('|',1)):tuple(v) for k,v in obj['transitions'].items()}
    return MealyMachine(tuple(obj['states']),tuple(obj['inputs']),tuple(obj['outputs']),obj['initial'],t)
def machine_to_json(m):
    return json.dumps({'states':list(m.states),'inputs':list(m.inputs),'outputs':list(m.outputs),'initial':m.initial,'transitions':[{'source':q,'input':a,'destination':p,'output':o} for (q,a),(p,o) in m.transitions.items()]},indent=2)
def machine_from_json(data):
    obj=json.loads(data); t={}
    for x in obj['transitions']:
        k=(x['source'],x['input'])
        if k in t: raise ValueError(f'Duplicate transition for {k}.')
        t[k]=(x['destination'],x['output'])
    return MealyMachine(tuple(obj['states']),tuple(obj['inputs']),tuple(obj['outputs']),obj['initial'],t)
def mealy_csv(m): return pd.DataFrame([{'State':q,'Input':a,'Next state':p,'Output':o} for (q,a),(p,o) in m.transitions.items()]).to_csv(index=False)
def moore_csv(m): return pd.DataFrame([{'State':s.name,'Output':s.output,'Input':a,'Next state':m.transitions[(s.name,a)]} for s in m.states for a in m.inputs if (s.name,a) in m.transitions]).to_csv(index=False)
