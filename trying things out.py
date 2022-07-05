new_dict = {'array': {0: {0: 1, 1: 2, 2: 3}, 1: {0: 1, 1: 7, 2: 5}}}

indices = [2]

value = 90

indices = [1]

def f(array, indices, value, level):
    if level == len(indices) - 1:
        array[indices[level]] = value
    else:
        f(array[indices[level]], indices, value, level + 1)

f(new_dict['array'], indices, value, 0)

print(new_dict)


