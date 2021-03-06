import inspect
import pickle

import classes
import races
from actions import attack_list
from aspects import character
from helper_functions import simple_choice

character.attack = attack_list  # This may be a group of actions eventually


def create_character():
    global char

    character.attack = attack_list  # This may be a group of actions eventually

    char = character()

    add_race_class()
    add_info()
    set_stats()
    add_other()

    first_equip()

    return char


def add_race_class():
    race_list = sorted([race[0].replace("_", " ") for race in
                        inspect.getmembers(races, inspect.isclass)
                        if not race[1].__subclasses__()])

    class_list = sorted([class_[0].replace("_", " ") for class_ in
                         inspect.getmembers(classes, inspect.isclass)
                         if issubclass(class_[1], classes.Class)
                         and not class_[1].__subclasses__()])

    class_choice = class_list[simple_choice(class_list)]
    classes.get_class(char, class_choice).add_class_features(char)

    race_choice = race_list[simple_choice(race_list)]
    races.get_race(char, race_choice).add_race_modifiers(char)

    char.update()

    return char


def add_info():
    # alignment
    # forename
    # middle name
    # family name

    char.update()


def set_stats():
    char.attributes.STR.base = 16
    char.attributes.DEX.base = 12
    char.attributes.CON.base = 14
    char.attributes.INT.base = 18
    char.attributes.WIS.base = 13
    char.attributes.CHA.base = 17

    char.update()


def add_other():
    from items import get_item

    char.equipment.update(
        {'Cloak of Protection': get_item('Cloak of Protection', 1)})

    char.update()


def first_equip():
    char.attune()
    char.equip()
    char.wield()

    char.update()


def export_info(name, info_object):
    try:
        info_object.update()
    except:
        print('Failed to update on export')

    loc = f'Character_sheet/saved/{name}'

    with open(loc + '.pkl', "wb") as file:
        pickle.dump(info_object, file, pickle.HIGHEST_PROTOCOL)
    file.close()


def import_info(name=None):
    if name:
        loc = f'Character_sheet/saved/{name}.pkl'
    else:
        ans = input("No name selected, choose from list?").lower()
        if ans in 'no':
            name = input("Choose file name:")
            if name != "":
                loc = f'Character_sheet/saved/{name}.pkl'
            else:
                pass  # list values
        else:
            pass  # list values
    file = open(loc, "rb")
    info = pickle.load(file)
    file.close()

    try:
        info.update()
    except:
        print('Failed to update on import')

    return info


def test_func():
    global char

    character.attack = attack_list  # This may be a group of actions eventually

    char = character()
    add_race_class()
    char.stats.current_hp = char.stats.max_hp
    # set_stats()
    # add_other()

    # first_equip()

    # saveas = input("Save as:")

    # export_info(saveas, char)
    return char


# char = import_info("Gorden")

# char = create_character()

char = test_func()

char.attributes.CHA.base = 18
char.update()
# export_info("Test", char)
# char = import_info("Test")
# char.wield()
# char.attack()

print(char.hp())
char.damage(20)
print(char.hp())

print("Done!")
