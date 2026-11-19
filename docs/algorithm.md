# Conversion algorithm

Let the Mealy machine be complete and deterministic. For each destination state `p`, define

`I(p) = { λ(q,a) : δ(q,a)=p }`.

Create a dedicated start state `S` with sentinel output `ε (initial)`. For every observed pair `(p,o)` with `o ∈ I(p)`, create a Moore state `(p,o)` whose output is `o`. For every input `a`, define

- `δ′(S,a) = (δ(q₀,a), λ(q₀,a))`;
- `δ′((q,o_prev),a) = (δ(q,a), λ(q,a))`.

The prior label is not used to choose the next transition; it distinguishes states that must have different Moore outputs. Starting at `S`, each consumed input takes the machine to a state labelled with precisely the output the Mealy transition emits. Induction on the input length proves output equality after dropping `S`'s sentinel. A BFS from `S` optionally removes unreachable variants.

```text
incoming[p] := set of outputs on transitions entering p
for p in Q, o in incoming[p]: create state (p,o), output=o
create S, output=ε(initial)
for a in Σ:
  δ′(S,a) := (δ(q₀,a), λ(q₀,a))
for every created (q,prev), a in Σ:
  δ′((q,prev),a) := (δ(q,a), λ(q,a))
BFS from S; optionally retain only reached states and edges
```

Time is `O(|Q||Σ| + |Q′||Σ|)` for complete transition generation and reachability; space is `O(|Q′||Σ|)`. Here `|Q′| ≤ 1 + |Q||Γ|`, more tightly bounded by the number of distinct incoming `(destination, output)` pairs plus one.
