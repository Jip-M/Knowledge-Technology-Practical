#
from typing import Literal


class Fact:
    def __init__(
        self, label: str, description: str, truth: int = -1, operator=None
    ) -> None:
        self._label = label
        self._description = description
        self._truth = truth
        self._operator = operator

    def set_truth(self, new_truth: Literal[0, 1]):
        self._truth = new_truth

    @property
    def truth(self):
        return self._truth


class Rule:
    def __init__(self, ifs: list[Fact], thens: list[Fact]):
        self._if: list[Fact] = ifs
        self._then: list[Fact] = thens

    def evaluate(self) -> None:
        for fact in self._if:
            if not fact.truth:
                return
        for fact in self._then:
            fact.set_truth(1)
        return
