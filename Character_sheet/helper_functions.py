from glossary import *
import textwrap
import functools
from feats import feats

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
    options = [option for option in true_options if option not in invalids]

    

    valid_choice = False

    print("\n", msg, "valid choices are:")
    print(textwrap.fill(", ".join(options), width = 80, initial_indent = '    ', subsequent_indent='    '))

    while not valid_choice:
        choice = input().upper()
        if choice in options:
            valid_choice = True
        else:
            print("Invalid Choice, valid choices are:")
            print(textwrap.fill(", ".join(options), width=80, initial_indent='    ', subsequent_indent='    '))
    
    return choice

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

def choose_feat(msg, self):

    feats_chosen = self.feats

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

def add_Modifier(self, modifier):
    aspect = vars(modifier)['aspect']
    value = vars(modifier)['value']
    rsetattr(self, aspect, value)

def add_Note(self, note):
    aspect = vars(note)['aspect']
    note = vars(note)['note']
    rsetattr(self, aspect, note)

def add_Feature(self, feature):
    aspect = vars(feature)['aspect']
    item = vars(feature)['item']
    rsetattr(self, aspect, item)


def add_feat(self, origin, name):
    name = name.lower().replace(" ", "_")
    
    if feats[name].prereq == False:
        rsetattr(self.feats, origin, feats[name])
        add_feat_features(self, feats[name])
    else:
        req_type = feats[name].prereq[0]
        req_val =  feats[name].prereq[1]
        if req_type == "armor":
            groups = (vars(self.profficiencies.armor).values())
            armors = set([armor for group in groups for armor in group])
            if req_val in armors:
                rsetattr(self.feats, origin, feats[name])
    return self

### Add prereq to feat choosing

def add_feat_features(self, feat):
    for effect in self.feats.race.effects:
        effect_type = type(effect).__name__
        if effect_type == "Modifier":
            add_Modifier(self, effect)
        elif effect_type == "Note":
            add_Note(self, effect)
        elif effect_type == "Feature":
            add_Feature(self, effect)