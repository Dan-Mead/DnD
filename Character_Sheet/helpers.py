import Character_Sheet.reference.item_types as item_types
from Character_Sheet.reference.items import equipment, other_items

def list_all(class_value):
    list = []

    for subclass in class_value.__subclasses__():
        list.append(subclass)
        list.extend(list_all(subclass))

    return list

def list_end_values(class_value):

    list = list_all(class_value)

    new_list = []

    for item in list:
        if not item.__subclasses__():
            new_list.append(item)

    return new_list