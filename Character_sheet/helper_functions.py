import textwrap

import numpy as np

from glossary import common_languages, attrs, skills_dict, exotic_languages, \
    ordinals


def LDK(dct, string_list):
    """ List Dictionary Key
    Parses a list to get a location, used in place of dot notation"""

    value = dct

    for item in string_list:
        value = value[item]

    return value


def mod_calc(num):
    return np.floor((num - 10) / 2)


def isclasstype(obj, type):
    return type in get_bases(obj)


def get_bases(obj):
    return tuple([base.__name__ for base in obj.__class__.__bases__])


def reset(dict):
    for key, value in dict.items():
        dict[key] = None
    return dict


##########################################################################

def simple_choice(options_list):
    print("Choose from:")
    for n, option in enumerate(options_list):
        print(n, ":", option)

    valid_choice = False

    choice = (input("Please enter number:"))

    while not valid_choice:
        if choice == "":
            print("Invalid choice! Please choose from list.")
            choice = (input())
        elif int(choice) in range(len(options_list)):
            valid_choice = True
        else:
            print("Invalid choice! Please choose from list.")
            choice = (input())

    return int(choice)


def choose_language(msg, known,
                    base_options=common_languages + exotic_languages):
    print_options = [option for option in base_options if option not in known]
    true_options = [option.lower() for option in print_options]

    valid_choice = False

    print(msg, "valid choices are:")
    print(
        textwrap.fill(", ".join(print_options), width=80, initial_indent='    ',
                      subsequent_indent='    '),
        "or 'none'.")

    while not valid_choice:

        choice = input()
        if choice.lower() in true_options:
            valid_choice = True
        elif choice == "" or choice == " ":
            valid_choice = True
            choice = None
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(print_options), width=80,
                                initial_indent='    ',
                                subsequent_indent='    '))

    return choice


def choose_stat(msg, invalid=None):
    if invalid is None:
        invalid = []
    print_options = [option for option in attrs if option not in invalid]
    true_options = print_options.copy()

    valid_choice = False

    print(msg, "valid choices are:")
    print(
        textwrap.fill(", ".join(print_options), width=80, initial_indent='    ',
                      subsequent_indent='    '))

    while not valid_choice:

        choice = input().upper()
        if choice in true_options:
            valid_choice = True
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(print_options), width=80,
                                initial_indent='    ',
                                subsequent_indent='    '))

    return choice


def choose_skill(msg, invalid=None):
    if invalid is None:
        invalid = []
    print_options = [skills_dict[option][0] for option in skills_dict if
                     option not in invalid]

    true_options = [option for option in skills_dict if option not in invalid]

    valid_choice = False

    print(msg, "valid choices are:")
    print(
        textwrap.fill(", ".join(print_options), width=80, initial_indent='    ',
                      subsequent_indent='    '))

    while not valid_choice:

        choice = input().lower().replace(" ", "_")
        if choice in true_options:
            valid_choice = True
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(print_options), width=80,
                                initial_indent='    ',
                                subsequent_indent='    '))

    return choice


def choose_feat(msg, char):
    from feats import get_valid_feats
    valid_feats = get_valid_feats(char)

    if char.feats:
        chosen = [feat.name for feat in char.feats.values()]
    else:
        chosen = []

    print_options = [feat for feat in valid_feats if feat not in chosen]
    true_options = [feat.lower().replace(" ", "_") for feat in print_options]
    valid_choice = False

    print(msg, "valid choices are:")
    print(
        textwrap.fill(", ".join(print_options), width=80, initial_indent='    ',
                      subsequent_indent='    '))

    while not valid_choice:

        choice = input().lower().replace(" ", "_")
        if choice in true_options:
            valid_choice = True
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(print_options), width=80,
                                initial_indent='    ',
                                subsequent_indent='    '))

    choice = dict(zip(true_options, print_options))[choice]

    return choice


##########################################################################

def add_language(char_languages, default, num_lang):
    lang_list = [default]
    for n in range(num_lang):
        new_lang = choose_language(
            "Choose " + ordinals[len(lang_list)].lower() + " language,",
            [default] + list(char_languages.values()))
        lang_list.append(new_lang)

    return list(filter(None, lang_list))


def add_attributes(allowed, num_attr):
    # TODO: Possibly need to include adding scores other than 1.

    attrs_list = []
    for n in range(num_attr):
        attrs_list.append(choose_stat(
            "Choose " + ordinals[n].lower() + "ability score to increase,",
            attrs_list))

    return list(zip(attrs_list, [1] * len(attrs_list)))


def add_skill(char_skills, allowed, num_skills):
    skills_list = []

    invalids = [skill for skill in char_skills if
                char_skills[skill]['prof'] == True]

    invalids += [skill for skill in char_skills.keys() if skill not in allowed]

    for n in range(num_skills):
        skills_list.append(choose_skill(
            "Choose " + ordinals[n].lower() + " skill to gain profficiency in,",
            invalids))
        invalids += skills_list
    return skills_list


def add_feat(char, num_feats):
    feats_list = []

    for n in range(num_feats):
        feats_list.append(choose_feat("Choose a feat,", char))

    return feats_list


def choose_weapons(equipment_list):
    from items import get_items

    weapon_list = {}
    for weapon in get_items('Weapon').items():
        weapon_list[weapon[0]] = weapon[1].get_weapon_type()

    for n, item in enumerate(equipment_list):
        if item[0] == 'Weapon':
            choices = []
            for weapon in weapon_list.keys():
                if item[2] in ['Any', weapon_list[weapon][0]]:
                    if item[3] in ['Any', weapon_list[weapon][1]]:
                        choices.append(weapon)
            choice = choices[simple_choice(choices)]
            equipment_list[n] = (choice, item[1])

    return equipment_list
