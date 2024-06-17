import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'
# Sample data
samples = ['A', 'B', 'C', 'D']
method1_10 = [23460, 8724, 58614, 14735]
method2_10 = [252, 161, 391, 2851]

method1 = [218, 77, 475, 97]
method2 = [27, 17, 40, 25]

ratio1 = [int((method1_10[i] - method1[i]) / method1[i] * 100) for i  in range(4)]
ratio2 = [int((method2_10[i] - method2[i]) / method2[i] * 100) for i  in range(4)]

# Setting positions and width for the bars
x = np.arange(len(samples))  # the label locations
width = 0.4  # the width of the bars
offset = 0.05

# Plotting the bars
fig, ax = plt.subplots(figsize=(8, 6))
ax.grid(axis='y', linestyle=':', linewidth=0.7)
bars1 = ax.bar(x - width/2, ratio1, width - offset, label='A*', edgecolor='black', linewidth=1)
bars2 = ax.bar(x + width/2, ratio2, width - offset, label='LLM-A*', edgecolor='black', linewidth=1)

# Adding text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('Samples')
ax.set_ylabel('Operation Increase Rate (%)')
ax.set_title('Operation Increase Ratio (%) on x10 Map Size')
ax.set_xticks(x)
ax.set_xticklabels(samples)
ax.legend(loc='upper left', fontsize=15)

# Adding labels on top of the bars
ax.bar_label(bars1, padding=3, fmt='  %.2i%%')
ax.bar_label(bars2, padding=3, fmt='  %.2i%%')

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0f}%'.format(y)))
# Display the plot
plt.savefig('plot_operation_rate.png')


#------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
ax.grid(axis='y', linestyle=':', linewidth=0.7)
bars1 = ax.bar(x - width/2, method1, width - offset, label='A*', edgecolor='black', linewidth=1)
bars2 = ax.bar(x + width/2, method2, width - offset, label='LLM-A*', edgecolor='black', linewidth=1)

# Adding text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('Samples')
ax.set_ylabel('Number of Operation')
ax.set_title('Operation on 50 x 30 Map')
ax.set_xticks(x)
ax.set_xticklabels(samples)
ax.legend(loc='upper left', fontsize=15)

# Adding labels on top of the bars
ax.bar_label(bars1, padding=3)
ax.bar_label(bars2, padding=3)

# Display the plot
plt.savefig('plot_operation_50_30.png')


#------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
ax.grid(axis='y', linestyle=':', linewidth=0.7)
bars1 = ax.bar(x - width/2, method1_10, width - offset, label='A*', edgecolor='black', linewidth=1)
bars2 = ax.bar(x + width/2, method2_10, width - offset, label='LLM-A*', edgecolor='black', linewidth=1)

# Adding text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('Samples')
ax.set_ylabel('Number of Operation')
ax.set_title('Operation on 500 x 300 Map')
ax.set_xticks(x)
ax.set_xticklabels(samples)
ax.legend(loc='upper left', fontsize=15)

# Adding labels on top of the bars
ax.bar_label(bars1, padding=3)
ax.bar_label(bars2, padding=3)

# Display the plot
plt.savefig('plot_operation_500_300.png')