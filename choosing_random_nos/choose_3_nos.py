max_number = 99
num_iterations = 1000000
running_sum = 0
nums_to_choose = 2
sum_list = []


import random

for i in range(num_iterations):
    base_list = [i for i in range(1, max_number)]
    nums_chosen = []
    for _ in range(nums_to_choose):
       nums_chosen.append(base_list[random.randint(0, len(base_list) - 1)])
       base_list.remove(nums_chosen[-1])
    sum_list.append(sum(nums_chosen))

f = open('output.csv', 'w')
f.write('\n'.join([str(x) for x in sum_list]))
f.close()