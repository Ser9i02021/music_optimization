import numpy as np
from lxml import etree
from label_chosen_licks import select_N_lick_samples 


licks_list = select_N_lick_samples(5)

for i in range(len(licks_list)):
    print(licks_list[i])

cost_matrix = np.full((4, 4), 100)

for i in range(len(licks_list)):
    for j in range(len(licks_list)):
        if i != j:
            all_false = True
            # T1
            if "C1" in licks_list[i][2] and ("C1" not in licks_list[j][2]):
                cost_matrix[i][j] = -50
                print("cost_matrix[{}][{}]: T1".format(i, j))
                all_false = False
            # T2
            if not (("C2" in licks_list[i][2]) or ("C3" in licks_list[i][2]) or ("C4" in licks_list[i][2])) and ("C2" in licks_list[j][2]):
                cost_matrix[i][j] = -15
                print("cost_matrix[{}][{}]: T2".format(i, j))
                all_false = False
            # T3
            if ("C2" in licks_list[i][2]) and (("C5" in licks_list[j][2]) or ("C6" in licks_list[j][2]) or ("C7" in licks_list[j][2])):
                cost_matrix[i][j] = -15
                print("cost_matrix[{}][{}]: T3".format(i, j))
                all_false = False
            # T4
            if licks_list[i][1][0] != "R" and licks_list[j][1][0] != "R": # Certify that none of the licks are a rest
                if (((ord(licks_list[i][1][0]) - 2) % 7) == ((ord(licks_list[i][1][0]) - 3) % 7)) and  licks_list[i][1][1] == licks_list[j][1][1]:
                    cost_matrix[i][j] = -15
                    print("cost_matrix[{}][{}]: T4".format(i, j))
                    all_false = False
            # T5
            if licks_list[i][1] == licks_list[j][0]:
                cost_matrix[i][j] = -15
                print("cost_matrix[{}][{}]: T5".format(i, j))
                all_false = False
            # T6
            if "C3" in licks_list[i][2] and "C6" in licks_list[j][2]:
                cost_matrix[i][j] = 25
                print("cost_matrix[{}][{}]: T6".format(i, j))
                all_false = False
            # T7
            if "C4" in licks_list[i][2] and ("C4" not in licks_list[j][2]):
                cost_matrix[i][j] = 25
                print("cost_matrix[{}][{}]: T7".format(i, j))
                all_false = False
            # T8
            if "C7" in licks_list[j][2]:
                cost_matrix[i][j] = 25
                print("cost_matrix[{}][{}]: T8".format(i, j))
                all_false = False
            # T9 (May be removed later. It is being used to identify if the transition does not fit in any of the previous categories) 
            if all_false:
                print("cost_matrix[{}][{}]: T9".format(i, j))

            
for i in range(len(licks_list)):
    for j in range(len(licks_list)):
        print(cost_matrix[i][j], end=" ")
    print()

            























































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
