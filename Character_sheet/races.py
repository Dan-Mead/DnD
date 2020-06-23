import textwrap

STR = 0
DEX = 1
CON = 2
INT = 3
WIS = 4
CHA = 5

stats = [STR, DEX, CON, INT, WIS, CHA]
common_languages = ["Common", "Dwarvish", "Elvish", "Giant", "Gnomish", "Goblin", "Halfling", "Orcish"]
exotic_languages = ["Abyssal", "Celestial", "Draconic", "Deep Speech", "Infernal", "Primordial", "Sylvan", "Undercommon"]


def choose_stat(msg, invalids = []):

    true_options = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    options = true_options.copy()

    if len(invalids) > 0:
        for invalid in invalids:
            options.remove(true_options[invalid])

    valid_choice = False
    while not valid_choice:
        choice = input(msg).upper()
        if choice in options:
            valid_choice = True
            index = true_options.index(choice)
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(options), width=80, initial_indent='    ', subsequent_indent='    '))
    return index

def choose_language(msg, known_languages, options = common_languages + exotic_languages):

    options = [known for known in options if known not in known_languages]

    valid_choice = False
    while not valid_choice:
        choice = input(msg)
        if not options:
            valid_choice = True
        else:
            if choice in options:
                valid_choice = True
                choice = [choice]
            elif choice == "" or choice == " ":
                valid_choice = True
                choice = []
            else:
                wrapper = textwrap.TextWrapper(width = 80)
                print("Invalid Choice, valid choices are:")
                print(textwrap.fill(", ".join(options), width = 80, initial_indent = '    ', subsequent_indent='    '))
    return choice

class Race_traits:
    def __init__(self, race_name, size, speed, ability_scores, languages):
        self.race = race_name
        self.size = size
        self.speed = speed
        self.scores = ability_scores
        self.languages = languages

def create_race(race):
    race_traits = Race_traits

    if race == "Human":
        race_traits.race = "Human"
        race_traits.size = "Medium"
        race_traits.speed = 30
        race_traits.scores = [(STR, +1), (DEX, +1), (CON, +1), (INT, +1), (WIS, +1), (CHA, +1)]
        languages = ["Common"]
        second_language = choose_language("Choose second language: ", languages)
        race_traits.languages = languages + second_language

    elif race == "Human_Variant":
        race_traits.race = "Human (Variant)"
        race_traits.size = "Medium"
        race_traits.speed = 30
        score_1 = choose_stat("Choose first ability score to increase (STR, DEX, etc.): ")
        score_2 = choose_stat("Choose second ability score to increase (STR, DEX, etc.): ", [score_1])
        race_traits.ability_scores = [(score_1, +1),(score_2,+1)]
        languages = ["Common"]
        second_language = choose_language("Choose second language: ", languages)
        race_traits.languages = languages + second_language
        race_traits.skills = "Test"
    return race_traits

race_traits = create_race("Human_Variant")

print(race_traits.skills)