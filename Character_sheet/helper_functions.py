from glossary import *
import textwrap

def LDK(dic, string_list):
    """ List Dictionary Key
    Parses a list to get a location, used in place of dot notation"""

    value = dic

    for item in string_list:
        print(item)
        value = value[item]

    return value

def choose_language(msg, known, base_options = common_languages + exotic_languages):
    
    print_options = [option for option in base_options if option not in known.values()]
    true_options = [option.lower() for option in print_options]


    valid_choice = False

    print("\n", msg, "valid choices are:")
    print(textwrap.fill(", ".join(print_options), width = 80, initial_indent = '    ', subsequent_indent='    '), "or 'none'.")
    
    while not valid_choice:

        choice = input()
        if choice.lower() in true_options:
            valid_choice = True
        elif choice == "" or choice == " ":
            valid_choice = True
            choice = None
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(print_options), width=80, initial_indent='    ', subsequent_indent='    '))
    
    return choice

def choose_stat(msg, invalid = []):


    
    print_options = [option for option in attrs.keys() if option not in invalid]
    true_options = print_options.copy()

    valid_choice = False

    print("\n", msg, "valid choices are:")
    print(textwrap.fill(", ".join(print_options), width = 80, initial_indent = '    ', subsequent_indent='    '))
    
    while not valid_choice:

        choice = input()
        if choice.upper() in true_options:
            valid_choice = True
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(print_options), width=80, initial_indent='    ', subsequent_indent='    '))
    
    return choice

# def choose_skill