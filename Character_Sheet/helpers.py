
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

def list_syntax(items):
    if items:
        if len(items) == 1:
            return items[0]
        elif len(items) == 2:
            return " and ".join(items)
        else:
            return ", ".join(items[:-1]) + f", and {items[-1]}"
    else:
        return ""