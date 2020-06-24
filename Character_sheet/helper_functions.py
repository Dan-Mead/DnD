from glossary import *
import textwrap
import functools

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

# using wonder's beautiful simplification: https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects/31174427?noredirect=1#comment86638618_31174427

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))




def choose_stat(msg, invalids = []):

    true_options = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    options = true_options.copy()

    if len(invalids) > 0:
        for invalid in invalids:
            options.remove(true_options[invalid])

    valid_choice = False

    print("\n", msg, "valid choices are:")
    print(textwrap.fill(", ".join(options), width = 80, initial_indent = '    ', subsequent_indent='    '))

    while not valid_choice:
        choice = input().upper()
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

    print("\n", msg, "valid choices are:")
    print(textwrap.fill(", ".join(options), width = 80, initial_indent = '    ', subsequent_indent='    '), "or none.")
    while not valid_choice:
        choice = input()
        if not options:
            valid_choice = True
        else:
            if choice in options:
                valid_choice = True
            elif choice == "" or choice == " ":
                valid_choice = True
                choice = None
            else:
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

    print("\n", msg, "valid choices are:")
    print(textwrap.fill(", ".join(options), width = 80, initial_indent = '    ', subsequent_indent='    '))

    while not valid_choice:    
        choice = input().lower()
        if choice in true_options:
                valid_choice = True                
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(options), width = 80, initial_indent = '    ', subsequent_indent='    '))
    

    choice = choice.replace(" ", "_")

    return choice
    