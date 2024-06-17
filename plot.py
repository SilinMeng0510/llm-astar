import matplotlib.pyplot as plt
import numpy as np
import json, os

test_set = {0: [4], 1:[4], 2:[0], 10:[0, 4], 12:[0], 15:[0], 17:[0, 4], 19: [0]}
def compute_performance():
  fail_list = {}
  operations_astar = [[], [], [], [], [], []]
  operations_llm = [[], [], [], [], [], []]
  operations_gpt = [[], [], [], [], [], []]
  path_0 = 'outcome/A*/environment_51_31_maps_gpt3.5/'
  path_2 = 'outcome/A*/environment_101_61_maps_llama3/'
  path_4 = 'outcome/A*/environment_201_121_maps_llama3/'
  path_6 = 'outcome/A*/environment_301_181_maps_llama3/'
  path_8 = 'outcome/A*/environment_401_241_maps_llama3/'
  path_10 = 'outcome/A*/environment_501_301_maps_gpt3.5/'
  for i in test_set.keys():
    astar_0 = os.path.join(path_0, f"map_{i}")
    astar_2 = os.path.join(path_2, f"map_{i}")
    astar_4 = os.path.join(path_4, f"map_{i}")
    astar_6 = os.path.join(path_6, f"map_{i}")
    astar_8 = os.path.join(path_8, f"map_{i}")
    astar_10 = os.path.join(path_10, f"map_{i}")
    
    llm_0 = os.path.join('outcome/A*/environment_51_31_maps_llama3/', f"map_{i}")
    llm_2 = os.path.join('outcome/A*/environment_101_61_maps_llama3/', f"map_{i}")
    llm_4 = os.path.join('outcome/A*/environment_201_121_maps_llama3/', f"map_{i}")
    llm_6 = os.path.join('outcome/A*/environment_301_181_maps_llama3/', f"map_{i}")
    llm_8 = os.path.join('outcome/A*/environment_401_241_maps_llama3/', f"map_{i}")
    llm_10 = os.path.join('outcome/A*/environment_501_301_maps_llama3/', f"map_{i}")
    
    # gpt_0 = os.path.join('outcome/A*/environment_51_31_maps_gpt3.5_cot/', f"map_{i}")
    # gpt_2 = os.path.join('outcome/A*/environment_101_61_maps_gpt3.5/', f"map_{i}")
    # gpt_4 = os.path.join('outcome/A*/environment_201_121_maps_gpt3.5/', f"map_{i}")
    # gpt_6 = os.path.join('outcome/A*/environment_301_181_maps_gpt3.5/', f"map_{i}")
    # gpt_8 = os.path.join('outcome/A*/environment_401_241_maps_gpt3.5/', f"map_{i}")
    # gpt_10 = os.path.join('outcome/A*/environment_501_301_maps_gpt3.5_cot/', f"map_{i}")
    for index in test_set[i]:
      a_0 = os.path.join(astar_0, f"sample_{index}/metrics.json")
      a_2 = os.path.join(astar_2, f"sample_{index}/metrics.json")
      a_4 = os.path.join(astar_4, f"sample_{index}/metrics.json")
      a_6 = os.path.join(astar_6, f"sample_{index}/metrics.json")
      a_8 = os.path.join(astar_8, f"sample_{index}/metrics.json")
      a_10 = os.path.join(astar_10, f"sample_{index}/metrics.json")
      
      lm_0 = os.path.join(llm_0, f"sample_{index}/metrics.json") 
      lm_2 = os.path.join(llm_2, f"sample_{index}/metrics.json")
      lm_4 = os.path.join(llm_4, f"sample_{index}/metrics.json")
      lm_6 = os.path.join(llm_6, f"sample_{index}/metrics.json")
      lm_8 = os.path.join(llm_8, f"sample_{index}/metrics.json")
      lm_10 = os.path.join(llm_10, f"sample_{index}/metrics.json") 
      
      # pt_0 = os.path.join(gpt_0, f"sample_{index}/metrics.json")
      # pt_2 = os.path.join(gpt_2, f"sample_{index}/metrics.json")
      # pt_4 = os.path.join(gpt_4, f"sample_{index}/metrics.json")
      # pt_6 = os.path.join(gpt_6, f"sample_{index}/metrics.json")
      # pt_8 = os.path.join(gpt_8, f"sample_{index}/metrics.json")
      # pt_10 = os.path.join(gpt_10, f"sample_{index}/metrics.json")
      
      with open(a_0, 'r') as file:
        as_0 = json.load(file)
      with open(a_2, 'r') as file:
        as_2 = json.load(file)
      with open(a_4, 'r') as file:
        as_4 = json.load(file)
      with open(a_6, 'r') as file:
        as_6 = json.load(file)
      with open(a_8, 'r') as file:
        as_8 = json.load(file)
      with open(a_10, 'r') as file:
        as_10 = json.load(file)
      
      with open(lm_0, 'r') as file:
        m_0 = json.load(file)
      with open(lm_2, 'r') as file:
        m_2 = json.load(file)
      with open(lm_4, 'r') as file:
        m_4 = json.load(file)
      with open(lm_6, 'r') as file:
        m_6 = json.load(file)
      with open(lm_8, 'r') as file:
        m_8 = json.load(file)
      with open(lm_10, 'r') as file:
        m_10 = json.load(file)
      
      # with open(pt_0, 'r') as file:
      #   g_0 = json.load(file)
      # with open(pt_2, 'r') as file:
      #   g_2 = json.load(file)
      # with open(pt_4, 'r') as file:
      #   g_4 = json.load(file)
      # with open(pt_6, 'r') as file:
      #   g_6 = json.load(file)
      # with open(pt_8, 'r') as file:
      #   g_8 = json.load(file)
      # with open(pt_10, 'r') as file:
      #   g_10 = json.load(file)
      
      # gpt_result_0 = g_0['llm']["operation"]
      # gpt_result_2 = g_2['llm']["operation"]
      # gpt_result_4 = g_4['llm']["operation"]
      # gpt_result_6 = g_6['llm']["operation"]
      # gpt_result_8 = g_8['llm']["operation"]
      # gpt_result_10 = g_10['llm']["operation"]
      
      llm_result_0 = m_0['llm']["operation"]
      llm_result_2 = m_2['llm']["operation"]
      llm_result_4 = m_4['llm']["operation"]
      llm_result_6 = m_6['llm']["operation"]
      llm_result_8 = m_8['llm']["operation"]
      llm_result_10 = m_10['llm']["operation"]
      
      astar_result_0 = as_0['astar']["operation"]
      astar_result_2 = as_2['astar']["operation"]
      astar_result_4 = as_4['astar']["operation"]
      astar_result_6 = as_6['astar']["operation"]
      astar_result_8 = as_8['astar']["operation"]
      astar_result_10 = as_10['astar']["operation"]
      
      
      operations_astar[0].append(astar_result_0)
      operations_astar[1].append(astar_result_2)
      operations_astar[2].append(astar_result_4)
      operations_astar[3].append(astar_result_6)
      operations_astar[4].append(astar_result_8)
      operations_astar[5].append(astar_result_10)
      
      operations_llm[0].append(llm_result_0)
      operations_llm[1].append(llm_result_2)
      operations_llm[2].append(llm_result_4)
      operations_llm[3].append(llm_result_6)
      operations_llm[4].append(llm_result_8)
      operations_llm[5].append(llm_result_10)
      
      # operations_gpt[0].append(gpt_result_0)
      # operations_gpt[1].append(gpt_result_2)
      # operations_gpt[2].append(gpt_result_4)
      # operations_gpt[3].append(gpt_result_6)
      # operations_gpt[4].append(gpt_result_8)
      # operations_gpt[5].append(gpt_result_10)
  return (operations_astar, operations_llm, operations_gpt)

plt.rcParams['font.family'] = 'serif'
plt.rcParams["font.serif"] =  ["DejaVu Serif"]
# Example data: replace with your actual data

# Hypothetical number of operations for each map size (multiple samples)
answer = compute_performance()
# print(answer)
operations_astar, operations_llm, operations_gpt = answer[0], answer[1], answer[2]
new_operations_astar, new_operations_llm, new_operations_gpt = [], [], []
for operation in operations_astar:
  new_operations_astar.append([operation[i] / operations_astar[0][i] for i in range(len(operation))])
for operation in operations_llm:
  new_operations_llm.append([operation[i] / operations_llm[0][i] for i in range(len(operation))])
# for operation in operations_gpt:
#   new_operations_gpt.append([operation[i] / operations_gpt[0][i] for i in range(len(operation))])

for operation in new_operations_llm:
  print(operation)
print(f'astar median: {[np.mean(op) for op in new_operations_astar]}')
print(f'llm median: {[np.mean(op) for op in new_operations_llm]}')
# print(f'gpt median: {[np.mean(op) for op in new_operations_gpt]}')


# Create the plot
plt.figure(figsize=(8, 12))
# Data
map_sizes = [1, 2, 4, 6, 8, 10]

plt.subplot(211)
means = [np.mean(op) for op in new_operations_astar]
A_star_op = means
plt.errorbar(map_sizes, means, fmt='o', capsize=5, label='A*', linestyle='-', color='#1f77b4', markersize=7)

means = [np.mean(op) for op in new_operations_llm]
LLM_A_star_op = means
plt.errorbar(map_sizes, means, fmt='o', capsize=5, label='LLM-A* (Ours)', linestyle='-', color='#ff7f0e', markersize=7)

plt.xticks([1, 2, 4, 6, 8, 10], fontsize=17)
plt.yticks(fontsize=17)
# plt.yscale('log')
plt.xlabel('Number of Scale', fontsize=20)
plt.ylabel('Growth Factor of Operations', fontsize=18)
plt.annotate('(a) OPEARTION', xy=(0.5, -0.23), xycoords='axes fraction', ha='center', fontsize=20, weight='bold')
plt.grid(True, linestyle=':')
plt.legend(loc='upper left', fontsize=25)


plt.subplot(212)
storage_astar =  [1.0, 3.176597282153432, 11.312836688973496, 24.408312055508848, 42.44017020736437, 65.44665851263778]
means = storage_astar
plt.errorbar(map_sizes, means, fmt='o', capsize=5, label='A*', linestyle='-', color='#1f77b4', markersize=7)

storage_llm =  [1.0, 2.3674573345192917, 4.778719761545509, 11.148485292114989, 11.671644775208236, 14.33979388956828]
means = storage_llm
plt.errorbar(map_sizes, means, fmt='o', capsize=5, label='LLM-A* (Ours)', linestyle='-', color='#ff7f0e', markersize=7)

plt.xticks([1, 2, 4, 6, 8, 10], fontsize=17)
plt.yticks(fontsize=17)
# plt.yscale('log')
plt.xlabel('Number of Scale', fontsize=20)
plt.ylabel('Growth Factor of Storages', fontsize=18)
plt.annotate('(b) STORAGE', xy=(0.5, -0.23), xycoords='axes fraction', ha='center', fontsize=20, weight='bold')
plt.grid(True, linestyle=':')
plt.legend(loc='upper left', fontsize=25)

plt.tight_layout()
plt.subplots_adjust(hspace=0.32)
# Show the plot
plt.savefig('plot.pdf')
