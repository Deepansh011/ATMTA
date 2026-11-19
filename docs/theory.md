# Theory notes

A deterministic Mealy machine is `M=(Q,Σ,Γ,δ,λ,q₀)`, with transition function `δ:Q×Σ→Q` and transition output function `λ:Q×Σ→Γ`. Completeness means both functions are defined for every state and input pair.

A deterministic Moore machine is `M′=(Q′,Σ,Γ,δ′,λ′,q′₀)`, where `λ′:Q′→Γ` attaches output to states. Under the common run convention used here, its output sequence includes `λ′(q′₀)` before any input is read. Thus a word of length `n` gives `n` Mealy outputs and `n+1` Moore state outputs. The initial sentinel is omitted for comparison.

The state splitting construction stores the last output on the destination variant. Distinct labels require distinct variants because one Moore state cannot have multiple outputs. A state with no incoming transitions needs no variant, though the dedicated start state still represents the pre-input position.
