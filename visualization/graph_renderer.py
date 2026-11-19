import html

def dot_mealy(m):
    lines=['digraph G { rankdir=LR; graph [bgcolor="transparent"]; node [shape=circle,style=filled,fillcolor="#eff6ff",fontcolor="#1f2937",color="#2563eb"]; edge [color="#64748b",fontcolor="#1f2937"]; __start [shape=none,label=""]; __start -> '+q(m.initial)+';']
    for (s,a),(d,o) in m.transitions.items(): lines.append(f'{q(s)} -> {q(d)} [label="{a}/{o}"];')
    for s in m.states: lines.append(f'{q(s)} [label="{s}"];')
    return '\n'.join(lines+['}'])
def dot_moore(m):
    lines=['digraph G { rankdir=LR; graph [bgcolor="transparent"]; node [shape=circle,style=filled,fillcolor="#eff6ff",fontcolor="#1f2937",color="#2563eb"]; edge [color="#64748b",fontcolor="#1f2937"]; __start [shape=none,label=""]; __start -> '+q(m.initial)+';']
    for s in m.states: lines.append(f'{q(s.name)} [label="{s.name}\\n/ {s.output}"];')
    for (s,a),d in m.transitions.items(): lines.append(f'{q(s)} -> {q(d)} [label="{a}"];')
    return '\n'.join(lines+['}'])
def q(s): return '"'+str(s).replace('\\','\\\\').replace('"','\\"')+'"'
def svg_diagram(states, edges, initial, node_labels, edge_labels, title):
    # Deterministic circular layout, self-loop and parallel edges supported.
    import math
    n=max(1,len(states)); cx,cy,r=360,240,170; pos={s:(cx+r*math.cos(2*math.pi*i/n-math.pi/2),cy+r*math.sin(2*math.pi*i/n-math.pi/2)) for i,s in enumerate(states)}
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="480" viewBox="0 0 720 480"><rect width="100%" height="100%" fill="#ffffff"/><text x="24" y="34" fill="#1f2937" font-size="20">{html.escape(title)}</text><defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#64748b"/></marker></defs>']
    for i,(s,d,label) in enumerate(edges):
        x,y=pos[s]; X,Y=pos[d]
        if s==d: path=f'M{x-18},{y-25} C{x-75},{y-100} {x+75},{y-100} {x+18},{y-25}'; tx,ty=x,y-86
        else:
            dx,dy=X-x,Y-y; L=max(1,math.hypot(dx,dy)); ux,uy=dx/L,dy/L; path=f'M{x+ux*28},{y+uy*28} L{X-ux*30},{Y-uy*30}'; tx,ty=(x+X)/2,(y+Y)/2-8
        out.append(f'<path d="{path}" fill="none" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/><text x="{tx}" y="{ty}" fill="#1f2937" text-anchor="middle" font-size="13">{html.escape(label)}</text>')
    for s in states:
        x,y=pos[s]; out.append(f'<circle cx="{x}" cy="{y}" r="29" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="{x}" y="{y+4}" fill="#1f2937" text-anchor="middle" font-size="12">{html.escape(node_labels[s])}</text>')
        if s==initial: out.append(f'<text x="{x}" y="{y+48}" fill="#2563eb" text-anchor="middle" font-size="12">INITIAL</text>')
    out.append('</svg>')
    return ''.join(out)
def mealy_svg(m): return svg_diagram(list(m.states),[(s,d,f'{a} / {o}') for (s,a),(d,o) in m.transitions.items()],m.initial,{s:s for s in m.states},{},'Mealy machine · edge outputs')
def moore_svg(m): return svg_diagram([s.name for s in m.states],[(s,d,a) for (s,a),d in m.transitions.items()],m.initial,{s.name:f'{s.name} / {s.output}' for s in m.states},{},'Moore machine · state outputs')
