import numpy as np
from lxml import etree
from label_chosen_licks import select_N_lick_samples 


licks_list = select_N_lick_samples(5)

print(licks_list)

cost_matrix = np.full((4, 4), 100)

for i in range(len(licks_list)):
    for j in range(len(licks_list)):
        if i != j:
            # T1
            if "C1" in licks_list[i][2] and ("C1" not in licks_list[j][2]):
                cost_matrix[i][j] = -50
                print("cost_matrix[{}][{}]: T1".format(i, j))
            # T2
            if not (("C2" in licks_list[i][2]) or ("C3" in licks_list[i][2]) or ("C4" in licks_list[i][2])) and ("C2" in licks_list[j][2]):
                cost_matrix[i][j] = -15
                print("cost_matrix[{}][{}]: T2".format(i, j))
            # T3
            if ("C2" in licks_list[i][2]) and ("C5" in licks_list[j][2]) or ("C6" in licks_list[j][2]) or ("C7" in licks_list[j][2]):
                cost_matrix[i][j] = -15
                print("cost_matrix[{}][{}]: T3".format(i, j))
            # T4
            if (((ord(licks_list[i][1][0]) - 2) % 7) == ((ord(licks_list[i][1][0]) - 3) % 7)) and  licks_list[i][1][1] == licks_list[j][1][1]:
                cost_matrix[i][j] = -15
                print("cost_matrix[{}][{}]: T4".format(i, j))
            # T5
            if licks_list[i][1] == licks_list[j][0]:
                cost_matrix[i][j] = -15
                print("cost_matrix[{}][{}]: T5".format(i, j))
            # T6
            























































# Load XML file
tree = etree.parse(r"C:\Users\pc\Documents\TCC_I_dset\licks_dset_new\Turnaround_pause_start\5.xml")
root = tree.getroot()

# Print root tag
#print("Root tag:", root.tag)

# Finding elements using XPath
#for element in root.xpath("//item"):  # Adjust the XPath to your XML structure
#    print("Item:", element.text)

P = np.full((5, 5), 100)  


def assign_a_value_for_one_element():
    for i in range(5):
        for j in range(5):
            # T1
            if i == "rep":
                P[i][j] = -50
                return
            # T2
            elif i == "does not end with pause" and j == "ends with pause <= 1 beat":
                P[i][j] = -15
                return
            # T3
            elif i == "ends with pause <= 1 beat" and j == "starts with pause":
                P[i][j] = -15
                return
            # T4
            elif i == "ends with pause <= 1 beat" and j == "starts with pause":
                P[i][j] = -15
                return
            else:
                pass
