# print("Input the number of cards:")
from argparse import ArgumentParser
from io import StringIO
import argparse
class FlashcardsBox():

    def __init__(self, import_from='', export_to=''):

        self.flashcard_dict = {}
        self.stat_dict = {}
        self.output = StringIO()
        self.import_from = import_from
        self.export_to = export_to

    def add_function(self):

        print(f"The card:")
        print(f"The card:", file=self.output, flush=True)
        term = input()
        while term in self.flashcard_dict.keys():
            term = input(f"The card \"{term}\" already exists. Try again:\n")
            print(f"The card \"{term}\" already exists. Try again:", file=self.output, flush=True)
            print(f"{term}", file=self.output, flush=True)

        print(f"The definition of the card:")
        print(f"The definition of the card:", file=self.output, flush=True)
        definition = input()
        while definition in self.flashcard_dict.values():
            definition = input(f"The definition \"{definition}\" already exists. Try again:\n")
            print(f"The definition \"{definition}\" already exists. Try again:", file=self.output, flush=True)
            print(f"{definition}", file=self.output, flush=True)

        self.flashcard_dict.update({term: definition})
        self.stat_dict.update({term: 0})
        print(f"The pair (\"{term}\":\"{definition}\") has been added.")
        print(f"The pair (\"{term}\":\"{definition}\") has been added.", file=self.output, flush=True)

    def remove_function(self):

        print(f"Which card?")
        print(f"Which card?", file=self.output, flush=True)
        term = input()
        print(f"{term}", file=self.output, flush=True)
        try:
            del self.flashcard_dict[term]
        except KeyError:
            print(f"Can't remove \"{term}\": there is no such card.")
            print(f"Can't remove \"{term}\": there is no such card.", file=self.output, flush=True)
        else:
            print(f"The card has been removed.")
            print(f"The card has been removed.", file=self.output, flush=True)

    def import_function(self, initial_import=False):

        if not initial_import:
            print("File name:")
            print("File name:", file=self.output, flush=True)
            filename = input()
            print(f"{filename}", file=self.output, flush=True)
        else:
            filename = self.import_from

        update_counter = 0
        try:
            with open(filename, 'r') as savefile:
                while True:
                    line = savefile.readline()
                    if not line: break
                    term, definition, mistakes = line[:-1].split(sep=';;')
                    self.flashcard_dict.update({term: definition})
                    self.stat_dict.update(({term: int(mistakes)}))
                    update_counter += 1
            print(f"{update_counter} cards have been loaded.")
            print(f"{update_counter} cards have been loaded.", file=self.output, flush=True)

        except FileNotFoundError:
            print("File not found.")
            print("File not found.", file=self.output, flush=True)

    def export_function(self, exit_export=False):

        if not exit_export:
            print("File name:")
            print("File name:", file=self.output, flush=True)
            filename = input()
            print(f"{filename}", file=self.output, flush=True)
        else:
            filename = self.export_to

        with open(filename, 'w') as savefile:
            for a, b, c in zip(self.flashcard_dict.keys(), self.flashcard_dict.values(), self.stat_dict.values()):
                savefile.write(f"{a};;{b};;{c}\n")
        print(f"{len(self.flashcard_dict.keys())} cards have been saved.")
        print(f"{len(self.flashcard_dict.keys())} cards have been saved.", file=self.output, flush=True)

    def ask_function(self):

        print(f"How many times to ask?")
        print(f"How many times to ask?", file=self.output, flush=True)
        ask_reps = int(input())
        print(f"{ask_reps}", file=self.output, flush=True)
        counter = 0
        for n in range(ask_reps):
            term = list(self.flashcard_dict.keys())[n%len(self.flashcard_dict.keys())]
        # for term in self.flashcard_dict.keys():
        #     if counter >= ask_reps: break
            print(f"Print the definition of \"{term}\":")
            print(f"Print the definition of \"{term}\":", file=self.output, flush=True)
            ans = input()
            print(f"{ans}", file=self.output, flush=True)
            if ans == self.flashcard_dict[term]:
                print("Correct!")
                print("Correct!", file=self.output, flush=True)
                counter += 1
                continue
            elif ans in self.flashcard_dict.values():
                print(
                    f"Wrong. The right answer is \"{self.flashcard_dict[term]}\", but your definition is correct for \"{list(self.flashcard_dict.keys())[list(self.flashcard_dict.values()).index(ans)]}\".")
                print(f"Wrong. The right answer is \"{self.flashcard_dict[term]}\", but your definition is correct for \"{list(self.flashcard_dict.keys())[list(self.flashcard_dict.values()).index(ans)]}\".",
                      file=self.output,
                      flush=True)
            else:
                print(f"Wrong. The right answer is \"{self.flashcard_dict[term]}\".")
                print(f"Wrong. The right answer is \"{self.flashcard_dict[term]}\".",
                      file=self.output,
                      flush=True)
            self.stat_dict[term] += 1
            counter += 1

    def hardest_function(self):

        if all(val == 0 for val in self.stat_dict.values()):
            print(f"There are no cards with errors")
            print(f"There are no cards with errors", file=self.output, flush=True)
        else:
            sorted_scores = dict(sorted(self.stat_dict.items(), key=lambda item: item[1], reverse=True))
            highest_score = list(sorted_scores.values())[0]
            number_of_items = list(sorted_scores.values()).count(highest_score)
            highest_terms = list(sorted_scores.keys())[:number_of_items]
            highest_terms = [f"\"{term}\"" for term in highest_terms]
            if number_of_items == 1:
                print(f"The hardest card is {highest_terms[0]}. You have {highest_score} errors answering it")
                print(f"The hardest card is {highest_terms[0]}. You have {highest_score} errors answering it", file=self.output, flush=True)
            else:
                print(f"The hardest cards are ", end='')
                print(*highest_terms)
                print(f"The hardest cards are ", end='', file=self.output, flush=True)
                print(*highest_terms, end='', file=self.output, flush=True)

    def exit_function(self):
        if self.export_to:
            self.export_function(exit_export=True)
        print("Bye bye!")
        print("Bye bye!", file=self.output, flush=True)
        self.output.close()

    def log_function(self):
        print("File name:")
        print("File name:", file=self.output, flush=True)
        filename = input()
        print(f"{filename}", file=self.output, flush=True)
        with open(filename, 'w') as log:
            for line in self.output.getvalue():
                print(line, file=log, flush=True, end='')
        print("The log has been saved")
        print("The log has been saved", file=self.output, flush=True)

    def reset_function(self):
        self.stat_dict = {x: 0 for x in self.stat_dict}
        print("Card statistics have been reset")
        print("Card statistics have been reset", file=self.output, flush=True)

    def initial_import(self):
        self.import_function(initial_import=True)

    def command_info(self):
        print(f"Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        print(f"Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):",
              file=self.output, flush=True)

    def execute(self, command):
        command_dict = {
            'add': self.add_function,
            'remove': self.remove_function,
            'import': self.import_function,
            'export': self.export_function,
            'ask': self.ask_function,
            'exit': self.exit_function,
            'log': self.log_function,
            'reset stats': self.reset_function,
            'hardest card': self.hardest_function,
            'initial_import': self.initial_import,
            'command_info': self.command_info
        }

        if command in command_dict.keys():
            command_dict[command]()
            if command == "exit":
                return
        else:
            return
        try:
            self.command_info()
        except ValueError:
            pass


parser = argparse.ArgumentParser()
parser.add_argument("--import_from", default='')
parser.add_argument("--export_to", default='')

args = parser.parse_args()

flash = FlashcardsBox(import_from=args.import_from, export_to=args.export_to)

if args.import_from:
    flash.execute("initial_import")
else:
    flash.command_info()

while True:
    command = input()
    flash.execute(command=command)
    if command == 'exit':
        break
