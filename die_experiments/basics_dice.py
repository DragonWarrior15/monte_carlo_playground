'''
simple die sum simulation using monte carlo
'''

import numpy as np
import matplotlib.pyplot as plt

num_die = 4
num_iterations = 100000
output_list = []
fig_name = str(num_die) + ' die throw simulation ' + str(num_iterations) + ' iterations.png'

for _ in range(num_iterations):
	curr_sum = 0
	for _ in range(num_die):
		curr_sum += np.random.randint(1, 7)
	output_list.append(curr_sum)

values, counts = np.unique(output_list, return_counts = True)

plt.figure()
plt.xticks(values)
plt.xlabel('Die Sums')
plt.ylabel('Counts')
plt.title(fig_name[:-4])
plt.bar(values, counts, align = 'center')
plt.savefig(fig_name, dpi = 300)

# f = open('die_output.csv', 'w')
# f.write('\n'.join([str(x) for x in output_list]))
# f.close()