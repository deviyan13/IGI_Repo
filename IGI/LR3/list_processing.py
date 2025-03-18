def product_of_even_elements(list):
    res = 1

    for i in range(0,len(list),2):
        res *= list[i]

    return res

def get_first_null_element_index(list):
    if 0 in list:
        return list.index(0)
    else:
        return -1

def get_last_null_element_index(list):
    if 0 in list:
        for i in reversed(range(len(list))):
            if list[i] == 0:
                return i
    else:
        return -1

def sum_of_elements(list, start_index, end_index):
    sum = 0
    for i in range(start_index, end_index + 1):
        sum += list[i]

    return sum
