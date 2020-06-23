from glossary import *
import textwrap


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

def choose_skill(msg, skills_list):
    options = []
    for skill in skills_list.__dict__:
        if getattr(skills_list, skill).prof == False:
            options.append(getattr(skills_list, skill).name)
    
    valid_choice = False

    true_options = [option.lower() for option in options]
    

    while not valid_choice:
        choice = input(msg).lower()
        if choice in true_options:
                valid_choice = True
                choice = [choice]

        else:
            wrapper = textwrap.TextWrapper(width = 80)
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(options), width = 80, initial_indent = '    ', subsequent_indent='    '))
    
    return choice
    