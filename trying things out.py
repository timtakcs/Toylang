new_dict = {'array': {0: {0: 1, 1: 2, 2: 3}, 1: {0: 1, 1: 7, 2: 5}}}

indices = [2]

value = 90

indices = [1, 1]

new_dict['array'][indices[0]][indices[1]] = value

print(new_dict)



