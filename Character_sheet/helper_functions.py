def LDK(dic, string_list):
    """ List Dictionary Key
    Parses a list to get a location, used in place of dot notation"""

    value = dic

    for item in string_list:
        print(item)
        value = value[item]

    return value