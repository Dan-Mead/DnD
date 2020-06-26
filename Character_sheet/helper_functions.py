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

def choose_feat(msg, feats_chosen):

    chosen = [origin.name for origin in vars(feats_chosen).values()]
    options = [feats[feat].name for feat in feats if feats[feat].name not in chosen]

    print("\n", msg, "valid choices are:")
    print(textwrap.fill(", ".join(options), width = 80, initial_indent = '    ', subsequent_indent='    '))

    valid_choice = False

    while not valid_choice:    
        choice = input().lower()
        if choice in [option.lower() for option in options]:
                valid_choice = True 
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(options), width = 80, initial_indent = '    ', subsequent_indent='    '))
    
    choice = choice.replace(" ", "_")

    return feats[choice].name

def add_feat(self, origin, name):
    
    name = name.lower().replace(" ", "_")
    
    if feats[name].prereq == False:
        rsetattr(self.feats, origin, feats[name])
        # add_feat_features(self, feats[name])
    else:
        req_type = feats[name].prereq[0]
        req_val =  feats[name].prereq[1]
        if req_type == "armor":
            groups = (vars(self.profficiencies.armor).values())
            armors = set([armor for group in groups for armor in group])
            if req_val in armors:
                rsetattr(self.feats, origin, feats[name])

    return self

def add_feat_features(self, feat):
    print(feat.effects)
