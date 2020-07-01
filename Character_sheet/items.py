import inspect
import items_list

def get_items(type_filter = None):

    from items_list import Item
    item_types = Item.__subclasses__()
    
    if type_filter:
        filter_val = getattr(items_list, type_filter)
        items = {}
        for item in (inspect.getmembers(items_list, inspect.isclass)):
            if filter_val in item[1].__mro__:
                items[item[0]] = item[1]
    else:
        items = {}
        for item in (inspect.getmembers(items_list, inspect.isclass)):
            if item[1] not in item_types:
                items[item[0].replace("_", " ")] = item[1]

    return items

def get_item(item_name, num):

    # item_list = get_items()
    items = get_items()

    item = items[item_name](num)


    if items_list.Pack in type(item).__bases__:
        item = item.contents ### TODO: Probably put this in some unpacking code.

    return item