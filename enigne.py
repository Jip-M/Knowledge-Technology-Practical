from typing import TypedDict
from typing import Literal
import json


class Rule(TypedDict):
    consequenct: str
    antecedent: dict[str, int]  # fact names


class Fact(TypedDict):
    name: str
    value: Literal[-1, 0, 1]


class Question(TypedDict):
    name: str
    question: str
    uniselect: bool
    asked: bool
    options: list[str]  # fact names


class KnowledgeBase(TypedDict):
    rules: list[Rule]
    facts: list[Fact]
    questions: list[Question]
    goals: list[Fact]


fact_values = Literal[-1, 0, 1]


class Engine:
    def __init__(self, json_path: str):
        self.kb = self._read_knowledge(json_path)

    def _read_knowledge(self, file_path: str) -> KnowledgeBase:
        with open(file_path, "r") as f:
            data = json.load(f)
        kb = KnowledgeBase()
        kb["rules"] = data["rules"]
        kb["questions"] = data["questions"]
        kb["facts"] = data["facts"]
        kb["goals"] = data["goals"]
        return kb

    def _is_goal_reached(self) -> tuple[bool, str]:
        for fact in self.kb["facts"]:
            if fact["name"] in self.kb["goals"] and fact["value"] == 1:
                return True, fact["name"]
        return False, "ugabuga"

    def _is_fact_value(self, fact_name: str, value: fact_values) -> bool:
        for fact in self.kb["facts"]:
            if fact["name"] == fact_name and fact["value"] == value:
                return True
        return False

    def _check_rule_antecedents(self, rule: Rule) -> bool:
        for key, value in rule["antecedent"].items():
            if not self._is_fact_value(key, value):
                return False
        return True

    def _check_rule_consequents(self, rule: Rule) -> bool:
        """
        CHecks if rule can produce new knowledge (if on of the consequents is not known).
        """
        for key in rule["consequent"]:
            if self._is_fact_value(key, -1):
                return True
        return False

    def _set_fact_value(self, fact_name: str, value: fact_values) -> None:
        for fact in self.kb["facts"]:
            if fact["name"] == fact_name:
                fact["value"] = value

    def _apply_rule(self, rule: Rule):
        for key, value in rule["consequent"].items():
            self._set_fact_value(key, value)

    def _apply_rules(self):
        for rule in self.kb["rules"]:
            if self._check_rule_consequents(rule) and self._check_rule_antecedents(rule):
                self._apply_rule(rule)

    def _is_question_useful(self, question: Question) -> bool:
        if question["asked"]:
            return False
        for fact_name in question["options"]:
            if self._is_fact_value(fact_name, -1):
                return True
        return False

    def _print_question(self, question: Question):
        print(question["question"])
        if not question["uniselect"]:
            print("This question is multiselect, input your different values and finish with #")
        for i, option in enumerate(question["options"]):
            print(f"({i}) {option}")
        print("######################\n")

    def _get_player_input(self, question: Question) -> list[str]:
        picked_options = []
        answer = "cringe"

        while answer != "#":
            answer = input("GIMME YOUR NUMBER: ")

            if answer.isdigit() and 0 <= int(answer) < len(question["options"]):
                picked_options.append(question["options"][int(answer)])
            elif answer != "#" or question["uniselect"]:
                print("INVALID INPUT")
                continue

            if question["uniselect"]:
                answer = "#"
        return picked_options

    def _act_upon_picked_options(self, picked_options: list[str], question: Question):
        for option in question["options"]:
            if option in picked_options:
                self._set_fact_value(option, 1)
            else:
                self._set_fact_value(option, 0)

    def _ask_question(self, question: Question) -> None:
        question["asked"] = True
        self._print_question(question)
        picked_options = self._get_player_input(question)
        self._act_upon_picked_options(picked_options, question)

    def _get_next_question(self) -> Question | None:
        for question in self.kb["questions"]:
            if self._is_question_useful(question):
                return question
        return None

    def forward_inf(self):
        while not self._is_goal_reached()[0]:
            self._ask_question(self._get_next_question())
            self._apply_rules()
        print(self._is_goal_reached()[1])


if __name__ == "__main__":
    e = Engine("knowledge.json")
    e.forward_inf()
