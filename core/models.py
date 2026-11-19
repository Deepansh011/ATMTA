from dataclasses import dataclass, field
from typing import Mapping

@dataclass(frozen=True)
class MealyMachine:
    states: tuple[str, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    initial: str
    transitions: Mapping[tuple[str, str], tuple[str, str]]

@dataclass(frozen=True)
class MooreState:
    name: str
    origin: str | None
    output: str
    initial: bool = False

@dataclass(frozen=True)
class MooreMachine:
    states: tuple[MooreState, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    initial: str
    transitions: Mapping[tuple[str, str], str]
    initial_output: str
    source_initial: str

    @property
    def state_map(self): return {s.name: s for s in self.states}
