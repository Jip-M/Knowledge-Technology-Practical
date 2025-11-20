
class Printer:
    def __init__(self, statement:str = "Hello world"):
        self._statement = statement

    def __call__(self):
        print(self._statement)

    def __repr__(self):
        return self._statement

    def update_statement(self, new_statement:str) -> None:
        self._statement = new_statement


myprinter = Printer()
myprinter()
print(myprinter)

class Rule:
    pass

class Fact:
    pass


