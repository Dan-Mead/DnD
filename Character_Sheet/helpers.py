import inspect


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


def subclasses(object):
    if inspect.isclass(object):
        return object.__subclasses__()
    else:
        return object.__class__.__subclasses__()


def weight_frame(frame):
    frame_width, frame_height = frame.grid_size()
    for n in range(frame_width):
        frame.columnconfigure(n, weight=1)
    for n in range(frame_height):
        frame.rowconfigure(n, weight=1)

def simple_print_dict(dict):
    for key, value in dict.items():
        print(key, value)

def simple_print_dict_sep(dict):
    for key, value in dict.items():
        print(key, "|", value)
