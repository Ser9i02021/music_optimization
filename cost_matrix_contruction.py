import numpy as np
from lxml import etree


# Load XML file
tree = etree.parse(r"C:\Users\pc\Documents\TCC_I_dset\licks_dset_new\Turnaround_pause_start\5.xml")
root = tree.getroot()

# Print root tag
print("Root tag:", root.tag)

# Finding elements using XPath
for element in root.xpath("//item"):  # Adjust the XPath to your XML structure
    print("Item:", element.text)

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