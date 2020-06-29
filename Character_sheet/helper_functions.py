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
    
    print_options = [option for option in base_options if option not in known]
    true_options = [option.lower() for option in print_options]


    valid_choice = False

    print(msg, "valid choices are:")
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

    print_options = [option for option in attrs if option not in invalid]
    true_options = print_options.copy()

    valid_choice = False

    print(msg, "valid choices are:")
    print(textwrap.fill(", ".join(print_options), width = 80, initial_indent = '    ', subsequent_indent='    '))
    
    while not valid_choice:

        choice = input().upper()
        if choice in true_options:
            valid_choice = True
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(print_options), width=80, initial_indent='    ', subsequent_indent='    '))
    
    return choice


def choose_skill(msg, invalid = []):

    print_options = [skills_dict[option][0] for option in skills_dict if option not in invalid]

    true_options = [option for option in skills_dict if option not in invalid]

    valid_choice = False

    print(msg, "valid choices are:")
    print(textwrap.fill(", ".join(print_options), width = 80, initial_indent = '    ', subsequent_indent='    '))
    
    while not valid_choice:

        choice = input().lower().replace(" ", "_")
        if choice in true_options:
            valid_choice = True
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(print_options), width=80, initial_indent='    ', subsequent_indent='    '))
    
    return choice

def choose_feat(msg, char):

    from feats import get_valid_feats, get_feats_list 
    valid_feats = get_valid_feats(char)
    feats_list = get_feats_list()

    # from feats import Shield_Master
    # char.feats['race'] = Shield_Master()

    if char.feats:
        chosen = [feat.name.lower().replace(" ", "_") for feat in char.feats.values()]
    else:
        chosen = []

    print_options = [feats_list[feat][0] for feat in valid_feats if feat not in chosen]
    true_options = [feat for feat in valid_feats if feat not in chosen]
    valid_choice = False
    
    print(msg, "valid choices are:")
    print(textwrap.fill(", ".join(print_options), width = 80, initial_indent = '    ', subsequent_indent='    '))

    while not valid_choice:

        choice = input().lower().replace(" ", "_")
        if choice in true_options:
            valid_choice = True
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(print_options), width=80, initial_indent='    ', subsequent_indent='    '))
    
    return choice