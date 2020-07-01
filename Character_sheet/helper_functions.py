from glossary import *
import textwrap
import inspect

def LDK(dic, string_list):
    """ List Dictionary Key
    Parses a list to get a location, used in place of dot notation"""

    value = dic

    for item in string_list:
        value = value[item]

    return value

##########################################################################

def simple_choice(options_list):

    print("Choose from:")
    for n, option in enumerate(options_list):
        print(n, ":", option)

    valid_choice = False

    choice = int(input("Please enter number:"))

    while not valid_choice:
        if choice in range(len(options_list)):
            return choice
            valid_choice = True
        else:
            print("Invalid choice! Please choose from list.")
            choice = int(input())

    return choice


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

##########################################################################

def add_language(char_languages, default, num_lang):

    lang_list = []
    lang_list.append(default)
    for n in range(num_lang):
        new_lang = choose_language("Choose " + ordinals[len(lang_list)].lower() + " language,", [default] + list(char_languages.values()))
        lang_list.append(new_lang)

    return list(filter(None, lang_list))

def add_attributes(allowed, num_attr):

    ## TODO: Possibly need to include adding scores other than 1.

    attrs_list = []
    for n in range(num_attr):
        attrs_list.append(choose_stat("Choose " + ordinals[n].lower() + " ability score to increase,", attrs_list))

    return list(zip(attrs_list, [1] * len(attrs_list)))

def add_skill(char_skills, allowed, num_skills):

    skills_list = []

    invalids = [skill for skill in char_skills if char_skills[skill]['prof'] == True]

    invalids += [skill for skill in char_skills.keys() if skill not in allowed ]

    for n in range(num_skills):
        skills_list.append(choose_skill("Choose " + ordinals[n].lower() + " skill to gain profficiency in,", invalids))
        invalids += skills_list
    return skills_list

def add_feat(char, num_feats):

    feats_list = []

    for n in range(num_feats):
        feats_list.append(choose_feat("Choose a feat,", char))

    return feats_list
    