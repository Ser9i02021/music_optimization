import random
import os
from lxml import etree


# Function to extract pitch information
def get_note_info(note):
    pitch = note.find("pitch")
    if pitch is not None:
        step = pitch.find("step").text  # Extracts the note name (e.g., F, G)
        octave = pitch.find("octave").text  # Extracts the octave number
        alter = pitch.find("alter")  # Checks for sharp (#) or flat (♭)

        # Convert alter to a string (if applicable)
        if alter is not None:
            alter_value = int(alter.text)
            if alter_value == 1:
                step += "#"  # Sharp note
            elif alter_value == -1:
                step += "♭"  # Flat note

        return f"{step}{octave}"
    else:
        duration = note.find("duration").text
        return "Rest w/ the duration (in beats) of " + duration

def lick_classification(lick_file_path: str):
    # Extract information from each lick and classify it from C1 to C9
    # ------------------------------------------------------------------------------
    # Otain first and last notes
    tree = etree.parse(lick_file_path)
    root = tree.getroot()

    # Find all <note> elements
    notes = root.findall(".//note")
    # Extract first and last note if available
    if notes:
        first_note = get_note_info(notes[0])
        last_note = get_note_info(notes[-1])
        #second_note = get_note_info(notes[1])
        print(f"First note: {first_note}")
        print(f"Last note: {last_note}")
        #print(f"Second note: {second_note}")
    else:
        print("No notes found in the XML file.")


    # ------------------------------------------------------------------------------
    # Classify it from C1 to C9
    lick_classes = []

    all_false = True

    # C1 (Repetition)


    # C2 (EwP <= 1)
    if last_note[0] == "R" and int(last_note[35:]) <= 1:
        print("EwP <= 1")
        lick_classes.append("C2")
        all_false = False

    # C3 (EwP > 1)
    if last_note[0] == "R" and int(last_note[35:]) > 1:
        print("EwP > 1")
        lick_classes.append("C3")
        all_false = False

    # C4 (Ewp > 2)    
    if last_note[0] == "R" and int(last_note[35:]) > 2:
        print("EwP > 2")
        lick_classes.append("C4")
        all_false = False

    # C5 (SwP <= 1)
    if first_note[0] == "R" and int(first_note[35:]) <= 1:
        print("SwP <= 1")
        lick_classes.append("C5")
        all_false = False

    # C6 (SwP > 1)
    if first_note[0] == "R" and int(first_note[35:]) > 1:
        print("SwP > 1")
        lick_classes.append("C6")
        all_false = False

    # C7 (SwP > 2)
    if first_note[0] == "R" and int(first_note[35:]) > 2:
        print("SwP > 2")
        lick_classes.append("C7")
        all_false = False

    # C8 (Turnaround)
    measure = root.find(".//measure")
    lick_label = measure.find("lick-label").text
    if lick_label == "turnaround":
        print("turnaround")
        lick_classes.append("C8")
        all_false = False

    # C9 (Regular)
    if all_false:
        print("any other (regular)")
        lick_classes.append("C9")


    lick = [first_note, last_note, lick_classes]  

    return lick





# Selection of N samples from the dataset (there must be at least 1 turnaround and 1 repetition licks, due to the problem hard constraints)
def select_N_lick_samples(n: int):
    lick_samples = []

    intial_dir = r"C:\Users\pc\Documents\TCC_I_dset\licks_dataset_sampling"
    FMS_dir = intial_dir + r"\FMS"
    rep_dir = intial_dir + r"\repetition"
    turn_dir = intial_dir + r"\turnaround"



    # List all files in the FSM directory 
    fsm_files = [f for f in os.listdir(FMS_dir) if os.path.isfile(os.path.join(FMS_dir, f))]


    # List all files in the repetition directory 
    rep_files = [f for f in os.listdir(rep_dir) if os.path.isfile(os.path.join(rep_dir, f))]


    # List all files in the turnaround directory 
    turn_files = [f for f in os.listdir(turn_dir) if os.path.isfile(os.path.join(turn_dir, f))]

    At_least_one_repetition = False
    At_least_one_turnaround = False

    for i in range(n):

        if i == n - 2 and (not (At_least_one_repetition and At_least_one_turnaround)): # Garantee that there is at least one repetition and one turnaround lick
            if not (At_least_one_repetition or At_least_one_turnaround): # Chose randomly one repetition and one turnaround licks in this order
                # Chose randomly one repetition lick
                if rep_files:
                    while True:
                        random_rep_file = random.choice(rep_files) 
                        random_rep_file_path = os.path.join(rep_dir, random_rep_file)
                        print("Randomly selected repetition lick file:", random_rep_file_path)

                        if random_rep_file_path not in lick_samples:
                            lick_samples.append(random_rep_file_path)
                            At_least_one_repetition = True
                            break
                        else:
                            continue
                else:
                    print("No files found in the folder.")

                # Chose randomly one turnaround lick
                if turn_files:
                    while True:
                        random_turn_file = random.choice(turn_files) 
                        random_turn_file_path = os.path.join(turn_dir, random_turn_file)
                        print("Randomly selected turnaround lick file:", random_turn_file_path)

                        if random_turn_file_path not in lick_samples:
                            lick_samples.append(random_turn_file_path)
                            At_least_one_turnaround = True
                            break
                        else:
                            continue
                else:
                    print("No files found in the folder.")
                
                break
            
            else:
                # If at least one repetition lick was chosen, one turnaround lick is randomly chosen
                if At_least_one_repetition:
                     # Ensure there are files in the folder
                    if turn_files:
                        while True:
                            random_turn_file = random.choice(turn_files) 
                            random_turn_file_path = os.path.join(turn_dir, random_turn_file)
                            print("Randomly selected turnaround lick file:", random_turn_file_path)

                            if random_turn_file_path not in lick_samples:
                                lick_samples.append(random_turn_file_path)
                                At_least_one_turnaround = True
                                break
                            else:
                                continue
                    else:
                        print("No files found in the folder.")
                
                # If at least one turnaround lick was chosen, one repetition lick is randomly chosen
                else:
                    '''
                    # Ensure there are files in the folder
                    if rep_files:
                        while True:
                            random_rep_file = random.choice(rep_files)  
                            random_rep_file_path = os.path.join(rep_dir, random_rep_file)
                            print("Randomly selected repetition lick file:", random_rep_file_path)

                            if random_rep_file_path not in lick_samples:
                                lick_samples.append(random_rep_file_path)
                                At_least_one_repetition = True
                                break
                            else:
                                continue
                    else:
                        print("No files found in the folder.")
                    '''
                    pass
        
        else:
            random_number = random.randint(331, 342) # For the random choice of a lick sample
            if random_number < 100: # Needs to be adjusted
                # Choose randomly a FSM lick
                if fsm_files:
                    while True:
                        random_fsm_file = random.choice(fsm_files) 
                        random_fsm_file_path = os.path.join(FMS_dir, random_fsm_file)
                        print("Randomly selected fsm lick file:", random_fsm_file_path)

                        if random_fsm_file_path not in lick_samples:    
                            lick_samples.append(random_fsm_file_path)
                            break
                        else:
                            continue
                else:
                    print("No files found in the folder.")

            # Choose randomly a repetition lick
            elif random_number >= 100 and random_number <= 330: # Needs to be adjusted (only 100)
                # Ensure there are files in the folder
                if rep_files:
                    while True:
                        random_rep_file = random.choice(rep_files)  
                        random_rep_file_path = os.path.join(rep_dir, random_rep_file)
                        print("Randomly selected repetition lick file:", random_rep_file_path)

                        if random_rep_file_path not in lick_samples:
                            lick_samples.append(random_rep_file_path)
                            At_least_one_repetition = True
                            break
                        else:
                            continue
                else:
                    print("No files found in the folder.")

            # Choose randomly a turnaround lick
            else:
                if turn_files:
                    while True:
                        random_turn_file = random.choice(turn_files) 
                        random_turn_file_path = os.path.join(turn_dir, random_turn_file)
                        print("Randomly selected turnaround lick file:", random_turn_file_path)

                        if random_turn_file_path not in lick_samples:
                            lick_samples.append(random_turn_file_path)
                            At_least_one_turnaround = True
                            break
                        else:
                            continue
                else:
                    print("No files found in the folder.")



    classified_licks = []
    # Classify the selected samples
    for lick in lick_samples:
        classified_lick = lick_classification(lick)
        classified_licks.append(classified_lick)

    return classified_licks

select_N_lick_samples(5) # Only 4 due to the fact that the repetition licks folder was not filled yet

