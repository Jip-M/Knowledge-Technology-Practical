import json
from copy import deepcopy
from enum import Enum
from typing import Literal, TypedDict

import streamlit as st

import ui


class Fact_value(Enum):
    true = 1
    false = 0
    unknown = -1


class Rule(TypedDict):
    consequent: str
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


fact_values = Fact_value  # Literal[-1, 0, 1]


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
            if (
                fact["name"] in self.kb["goals"]
                and fact["value"] == Fact_value.true.value
            ):
                return True, fact["name"]
        return False, "ugabuga"

    def _is_fact_value(self, fact_name: str, value: fact_values) -> bool:
        for fact in self.kb["facts"]:
            if fact["name"] == fact_name and fact["value"] == value:
                return True
        return False

    def _print_fact(self, fact_name: str) -> None:
        for fact in self.kb["facts"]:
            if fact["name"] == fact_name:
                print(f"{fact['name']}, ({fact['value']})")

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
            if self._is_fact_value(key, Fact_value.unknown.value):
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
        reapply = False
        for rule in self.kb["rules"]:
            if self._check_rule_consequents(rule) and self._check_rule_antecedents(
                rule
            ):
                self._apply_rule(rule)
                reapply = True
        if reapply:
            self._apply_rules()

    def _is_question_useful(self, question: Question) -> bool:
        if question["asked"]:
            return False
        for fact_name in question["options"]:
            if self._is_fact_value(fact_name, Fact_value.unknown.value):
                return True
        return False

    def _st_print_question(self, question: Question):
        if question["uniselect"]:
            selected = ui.uniselect(
                question["question"], options=question["options"], key=question["name"]
            )
        else:
            options = self._st_remove_options(question)
            selected = ui.multiselect(
                question["question"], options=options, key=question["name"]
            )
        # next = ui.next_question(f"{question['name']}_button", on_click=...)

        return selected

    def _st_remove_options(self, question: Question):
        copied_question = deepcopy(question)
        for option in question["options"]:
            if not self._is_fact_value(option, Fact_value.unknown.value):
                copied_question["options"].remove(option)
        return copied_question["options"]

    def _print_question(self, question: Question):
        print(question["question"])
        if not question["uniselect"]:
            print(
                "This question is multiselect, input your different values and finish with #"
            )
        copied_question = deepcopy(question)
        printed_index = 0
        for i, option in enumerate(question["options"]):
            # self._print_fact(option)
            if self._is_fact_value(option, Fact_value.unknown.value):
                print(f"({printed_index}) {option}")
                printed_index += 1
            else:
                copied_question["options"].pop(printed_index)
        print("######################\n")
        return copied_question

    def _get_player_input(self, printed_question: Question) -> list[str]:
        picked_options = []
        answer = "cringe"

        while answer != "#":
            answer = input("GIMME YOUR NUMBER: ")

            if answer.isdigit() and 0 <= int(answer) < len(printed_question["options"]):
                picked_options.append(printed_question["options"][int(answer)])
            elif answer != "#" or printed_question["uniselect"]:
                print("INVALID INPUT")
                answer = "cringe"
                continue

            if printed_question["uniselect"]:
                answer = "#"
        return picked_options

    def _act_upon_picked_options(
        self, picked_options: list[str] | None, question: Question
    ):
        if picked_options:
            for option in question["options"]:
                if option in picked_options:
                    self._set_fact_value(option, Fact_value.true.value)
                else:
                    self._set_fact_value(option, Fact_value.false.value)
                # self._print_fact(option)

    def _ask_question(self, question: Question) -> None:
        question["asked"] = True
        printed_questions = self._print_question(question)
        picked_options = self._get_player_input(printed_questions)
        self._act_upon_picked_options(picked_options, question)

    def _st_ask_question(self, question: Question) -> bool:
        question["asked"] = True
        picked_options = self._st_print_question(question)
        if question["uniselect"] and picked_options[0] is None:
            st.markdown("Please select an option above")
            return False
        self._act_upon_picked_options(picked_options, question)
        return True

    def _get_next_question(self) -> Question | None:
        for question in self.kb["questions"]:
            if self._is_question_useful(question):
                return question
        return None

    def _inference_failed(self) -> str:
        return "We apologise. We failed... :(\nthere is no house for you"

    # def _st_wait_for_user_input(
    #     self, question: Question, selected_options: list
    # ) -> bool:
    #     if question["uniselect"]:
    #         if selected_options is not None and ui.next_question(
    #             key=f"next_{question['name']}"
    #         ):
    #             return False
    #     else:
    #         if ui.next_question(key=f"next_{question['name']}"):
    #             return False
    #     return True

    def forward_inf(self):
        ui.general_ui()
        if not self._is_goal_reached()[0]:
            # next = st.checkbox(
            #     "next question",
            #     key=str(iterator),
            # )
            next_question = self._get_next_question()
            if not next_question:
                st.markdown(self._inference_failed())
                return None
            user_input = self._st_ask_question(next_question)
            self._apply_rules()
            st.markdown("")
            next = st.checkbox(
                "next question",
                key=f"{next_question['name']}_next",
            )
            if next and user_input:
                self.forward_inf()

        else:
            st.markdown(self._is_goal_reached()[1])
            st.balloons()
            print(self._is_goal_reached()[1])
            return None


if __name__ == "__main__":
    e = Engine("knowledge.json")
    e.forward_inf()
