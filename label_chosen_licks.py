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
    if lick_file_path.find("repetition") != -1:
        print("repetition")
        lick_classes.append("C1")
        all_false = False

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
    lick_label = measure.find("lick-label").text if measure.find("lick-label") is not None else None
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
    
    FSM_regular_fast = r"/Users/ser910/Downloads/licks_dataset_sampling/FMS/regular/fast"
    FSM_regular_moderate = r"/Users/ser910/Downloads/licks_dataset_sampling/FMS/regular/moderate"
    FSM_regular_slow = r"/Users/ser910/Downloads/licks_dataset_sampling/FMS/regular/slow"
    
    FSM_repetition_fast = r"/Users/ser910/Downloads/licks_dataset_sampling/FMS/repetition/fast"
    FSM_repetition_moderate = r"/Users/ser910/Downloads/licks_dataset_sampling/FMS/repetition/moderate"
    FSM_repetition_slow = r"/Users/ser910/Downloads/licks_dataset_sampling/FMS/repetition/slow"
    
    FSM_repetition_with_pause_fast = r"/Users/ser910/Downloads/licks_dataset_sampling/FMS/repetition_with_pause/fast"
    FSM_repetition_with_pause_moderate = r"/Users/ser910/Downloads/licks_dataset_sampling/FMS/repetition_with_pause/moderate"
    
    FSM_with_pause_fast = r"/Users/ser910/Downloads/licks_dataset_sampling/FMS/with_pause/fast"
    FSM_with_pause_moderate = r"/Users/ser910/Downloads/licks_dataset_sampling/FMS/with_pause/moderate"
    FSM_with_pause_slow = r"/Users/ser910/Downloads/licks_dataset_sampling/FMS/with_pause/slow"

    turnaround = r"/Users/ser910/Downloads/licks_dataset_sampling/turnaround"
    turnaround_with_pause = r"/Users/ser910/Downloads/licks_dataset_sampling/turnaround_with_pause"


    # List all files in the FSM directory 
    fsm_regular_fast_files = [f for f in os.listdir(FSM_regular_fast) if os.path.isfile(os.path.join(FSM_regular_fast, f))]
    fsm_regular_moderate_files = [f for f in os.listdir(FSM_regular_moderate) if os.path.isfile(os.path.join(FSM_regular_moderate, f))]
    fsm_regular_slow_files = [f for f in os.listdir(FSM_regular_slow) if os.path.isfile(os.path.join(FSM_regular_slow, f))]

    fsm_repetition_fast_files = [f for f in os.listdir(FSM_repetition_fast) if os.path.isfile(os.path.join(FSM_repetition_fast, f))]
    fsm_repetition_moderate_files = [f for f in os.listdir(FSM_repetition_moderate) if os.path.isfile(os.path.join(FSM_repetition_moderate, f))]
    fsm_repetition_slow_files = [f for f in os.listdir(FSM_repetition_slow) if os.path.isfile(os.path.join(FSM_repetition_slow, f))]

    fsm_repetition_with_pause_fast_files = [f for f in os.listdir(FSM_repetition_with_pause_fast) if os.path.isfile(os.path.join(FSM_repetition_with_pause_fast, f))]
    fsm_repetition_with_pause_moderate_files = [f for f in os.listdir(FSM_repetition_with_pause_moderate) if os.path.isfile(os.path.join(FSM_repetition_with_pause_moderate, f))]

    fsm_with_pause_fast_files = [f for f in os.listdir(FSM_with_pause_fast) if os.path.isfile(os.path.join(FSM_with_pause_fast, f))]
    fsm_with_pause_moderate_files = [f for f in os.listdir(FSM_with_pause_moderate) if os.path.isfile(os.path.join(FSM_with_pause_moderate, f))]
    fsm_with_pause_slow_files = [f for f in os.listdir(FSM_with_pause_slow) if os.path.isfile(os.path.join(FSM_with_pause_slow, f))]

    # List all files in the turnaround directory
    turnaround_files = [f for f in os.listdir(turnaround) if os.path.isfile(os.path.join(turnaround, f))]
    turnaround_with_pause_files = [f for f in os.listdir(turnaround_with_pause) if os.path.isfile(os.path.join(turnaround_with_pause, f))]

   
    At_least_one_repetition = False
    At_least_one_turnaround = False

    N = len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files) + len(fsm_repetition_with_pause_moderate_files)
    M = len(turnaround_files) + len(turnaround_with_pause_files)
    R = len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files)
    A = R + N + len(fsm_with_pause_fast_files) + len(fsm_with_pause_moderate_files) + len(fsm_with_pause_slow_files) + M

    q = 0
    while q < n: # (n >= 4)

        if (q == n - 3) and (not (At_least_one_repetition and At_least_one_turnaround)): # Garantee that there is at least one repetition and one turnaround lick
            if not (At_least_one_repetition or At_least_one_turnaround): # Chose randomly one repetition and one turnaround licks in this order
                # Chose randomly one repetition lick
                if fsm_repetition_fast_files and fsm_repetition_moderate_files and fsm_repetition_slow_files and fsm_repetition_with_pause_fast_files and fsm_repetition_with_pause_moderate_files:
                    while True:
                        random_number = random.randint(0, N - 1)
                        if random_number < len(fsm_repetition_fast_files):
                            random_rep_file = random.choice(fsm_repetition_fast_files) 
                            random_rep_file_path = os.path.join(FSM_repetition_fast, random_rep_file)
                        elif random_number >= len(fsm_repetition_fast_files) and random_number < len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files):
                            random_rep_file = random.choice(fsm_repetition_moderate_files) 
                            random_rep_file_path = os.path.join(FSM_repetition_moderate, random_rep_file)
                        elif random_number >= len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) and random_number < len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files):
                            random_rep_file = random.choice(fsm_repetition_slow_files) 
                            random_rep_file_path = os.path.join(FSM_repetition_slow, random_rep_file)
                        elif random_number >= len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) and random_number < len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files):
                            random_rep_file = random.choice(fsm_repetition_with_pause_fast_files)
                            random_rep_file_path = os.path.join(FSM_repetition_with_pause_fast, random_rep_file)
                        else:
                            random_rep_file = random.choice(fsm_repetition_with_pause_moderate_files)
                            random_rep_file_path = os.path.join(FSM_repetition_with_pause_moderate, random_rep_file)    
                        
                        print("Randomly selected repetition lick file:", random_rep_file_path)

                        if random_rep_file_path not in lick_samples:
                            lick_samples.append(random_rep_file_path)
                            At_least_one_repetition = True
                            break
                        else:
                            continue
                else:
                    print("No files found in the repetition folders.")

                # Chose randomly one turnaround lick
                if turnaround_files and turnaround_with_pause_files:
                    while True:
                        random_number = random.randint(0, M - 1)
                        if random_number < len(turnaround_files):
                            random_turn_file = random.choice(turnaround_files) 
                            random_turn_file_path = os.path.join(turnaround, random_turn_file)
                        else:
                            random_turn_file = random.choice(turnaround_with_pause_files) 
                            random_turn_file_path = os.path.join(turnaround_with_pause, random_turn_file)

                        print("Randomly selected turnaround lick file:", random_turn_file_path)

                        if random_turn_file_path not in lick_samples:
                            lick_samples.append(random_turn_file_path)
                            At_least_one_turnaround = True
                            break
                        else:
                            continue
                else:
                    print("No files found in the turnaround folders.")

                q += 1
                
            
            else:
                # If at least one repetition lick was chosen, one turnaround lick is randomly chosen
                if At_least_one_repetition:
                    if turnaround_files and turnaround_with_pause_files:
                        while True:
                            random_number = random.randint(0, M - 1)
                            if random_number < len(turnaround_files):
                                random_turn_file = random.choice(turnaround_files) 
                                random_turn_file_path = os.path.join(turnaround, random_turn_file)
                            else:
                                random_turn_file = random.choice(turnaround_with_pause_files) 
                                random_turn_file_path = os.path.join(turnaround_with_pause, random_turn_file)

                            print("Randomly selected turnaround lick file:", random_turn_file_path)

                            if random_turn_file_path not in lick_samples:
                                lick_samples.append(random_turn_file_path)
                                At_least_one_turnaround = True
                                break
                            else:
                                continue
                    else:
                        print("No files found in the turnaround folders.")
                    
                # If at least one turnaround lick was chosen, one repetition lick is randomly chosen
                else:
                    if fsm_repetition_fast_files and fsm_repetition_moderate_files and fsm_repetition_slow_files and fsm_repetition_with_pause_fast_files and fsm_repetition_with_pause_moderate_files:
                        while True:
                            random_number = random.randint(0, N - 1)
                            if random_number < len(fsm_repetition_fast_files):
                                random_rep_file = random.choice(fsm_repetition_fast_files) 
                                random_rep_file_path = os.path.join(FSM_repetition_fast, random_rep_file)
                            elif random_number >= len(fsm_repetition_fast_files) and random_number < len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files):
                                random_rep_file = random.choice(fsm_repetition_moderate_files) 
                                random_rep_file_path = os.path.join(FSM_repetition_moderate, random_rep_file)
                            elif random_number >= len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) and random_number < len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files):
                                random_rep_file = random.choice(fsm_repetition_slow_files) 
                                random_rep_file_path = os.path.join(FSM_repetition_slow, random_rep_file)
                            elif random_number >= len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) and random_number < len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files):
                                random_rep_file = random.choice(fsm_repetition_with_pause_fast_files)
                                random_rep_file_path = os.path.join(FSM_repetition_with_pause_fast, random_rep_file)
                            else:
                                random_rep_file = random.choice(fsm_repetition_with_pause_moderate_files)
                                random_rep_file_path = os.path.join(FSM_repetition_with_pause_moderate, random_rep_file)    
                            
                            print("Randomly selected repetition lick file:", random_rep_file_path)

                            if random_rep_file_path not in lick_samples:
                                lick_samples.append(random_rep_file_path)
                                At_least_one_repetition = True
                                break
                            else:
                                continue
                    else:
                        print("No files found in the repetition folders.")
                    
        else:
            if q == 0 or q == n - 1: # Make sure that the first and last licks are regular
                if fsm_regular_fast_files and fsm_regular_moderate_files and fsm_regular_slow_files:
                    while True:
                        random_number = random.randint(0, R - 1)
                        if random_number < len(fsm_regular_fast_files):
                            random_fsm_file = random.choice(fsm_regular_fast_files) 
                            random_fsm_file_path = os.path.join(FSM_regular_fast, random_fsm_file)
                        elif random_number >= len(fsm_regular_fast_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files):
                            random_fsm_file = random.choice(fsm_regular_moderate_files) 
                            random_fsm_file_path = os.path.join(FSM_regular_moderate, random_fsm_file)
                        else:
                            random_fsm_file = random.choice(fsm_regular_slow_files) 
                            random_fsm_file_path = os.path.join(FSM_regular_slow, random_fsm_file)

                        print("Randomly selected fsm lick file:", random_fsm_file_path)

                        if random_fsm_file_path not in lick_samples:
                            lick_samples.append(random_fsm_file_path)
                            break
                        else:
                            continue
                else:    
                    print("No files found in the regular folders.")

            else: # Chose randomly a lick of any type
                if fsm_regular_fast_files and fsm_regular_moderate_files and fsm_regular_slow_files and fsm_repetition_fast_files and fsm_repetition_moderate_files and fsm_repetition_slow_files and fsm_repetition_with_pause_fast_files and fsm_repetition_with_pause_moderate_files and fsm_with_pause_fast_files and fsm_with_pause_moderate_files and fsm_with_pause_slow_files and turnaround_files and turnaround_with_pause_files:
                    random_number = random.randint(0, A - 1) # For the random choice of a lick sample
                    while True:
                        if random_number < len(fsm_regular_fast_files):
                            random_file = random.choice(fsm_regular_fast_files)
                            random_file_path = os.path.join(FSM_regular_fast, random_file)
                            print("Randomly selected fsm_regular_fast lick file:", random_file_path)
                        elif random_number >= len(fsm_regular_fast_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files):
                            random_file = random.choice(fsm_regular_moderate_files)
                            random_file_path = os.path.join(FSM_regular_moderate, random_file)
                            print("Randomly selected fsm_regular_moderate lick file:", random_file_path)
                        elif random_number >= len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files):
                            random_file = random.choice(fsm_regular_slow_files)
                            random_file_path = os.path.join(FSM_regular_slow, random_file)
                            print("Randomly selected fsm_regular_slow lick file:", random_file_path)
                        elif random_number >= len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files):
                            random_file = random.choice(fsm_repetition_fast_files)
                            random_file_path = os.path.join(FSM_repetition_fast, random_file)
                            print("Randomly selected fsm_repetition_fast lick file:", random_file_path)
                        elif random_number >= len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files):
                            random_file = random.choice(fsm_repetition_moderate_files)
                            random_file_path = os.path.join(FSM_repetition_moderate, random_file)
                            print("Randomly selected fsm_repetition_moderate lick file:", random_file_path)
                        elif random_number >= len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files):
                            random_file = random.choice(fsm_repetition_slow_files)
                            random_file_path = os.path.join(FSM_repetition_slow, random_file)
                            print("Randomly selected fsm_repetition_slow lick file:", random_file_path)
                        elif random_number >= len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files):
                            random_file = random.choice(fsm_repetition_with_pause_fast_files)
                            random_file_path = os.path.join(FSM_repetition_with_pause_fast, random_file)
                            print("Randomly selected fsm_repetition_with_pause_fast lick file:", random_file_path)
                        elif random_number >= len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files) + len(fsm_repetition_with_pause_moderate_files):
                            random_file = random.choice(fsm_repetition_with_pause_moderate_files)
                            random_file_path = os.path.join(FSM_repetition_with_pause_moderate, random_file)
                            print("Randomly selected fsm_repetition_with_pause_moderate lick file:", random_file_path)
                        elif random_number >= len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files) + len(fsm_repetition_with_pause_moderate_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files) + len(fsm_repetition_with_pause_moderate_files) + len(fsm_with_pause_fast_files):
                            random_file = random.choice(fsm_with_pause_fast_files)
                            random_file_path = os.path.join(FSM_with_pause_fast, random_file)
                            print("Randomly selected fsm_with_pause_fast lick file:", random_file_path)
                        elif random_number >= len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files) + len(fsm_repetition_with_pause_moderate_files) + len(fsm_with_pause_fast_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files) + len(fsm_repetition_with_pause_moderate_files) + len(fsm_with_pause_fast_files) + len(fsm_with_pause_moderate_files):
                            random_file = random.choice(fsm_with_pause_moderate_files)
                            random_file_path = os.path.join(FSM_with_pause_moderate, random_file)
                            print("Randomly selected fsm_with_pause_moderate lick file:", random_file_path)
                        elif random_number >= len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files) + len(fsm_repetition_with_pause_moderate_files) + len(fsm_with_pause_fast_files) + len(fsm_with_pause_moderate_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files) + len(fsm_repetition_with_pause_moderate_files) + len(fsm_with_pause_fast_files) + len(fsm_with_pause_moderate_files) + len(fsm_with_pause_slow_files):
                            random_file = random.choice(fsm_with_pause_slow_files)
                            random_file_path = os.path.join(FSM_with_pause_slow, random_file)
                            print("Randomly selected fsm_with_pause_slow lick file:", random_file_path)
                        elif random_number >= len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files) + len(fsm_repetition_with_pause_moderate_files) + len(fsm_with_pause_fast_files) + len(fsm_with_pause_moderate_files) + len(fsm_with_pause_slow_files) and random_number < len(fsm_regular_fast_files) + len(fsm_regular_moderate_files) + len(fsm_regular_slow_files) + len(fsm_repetition_fast_files) + len(fsm_repetition_moderate_files) + len(fsm_repetition_slow_files) + len(fsm_repetition_with_pause_fast_files) + len(fsm_repetition_with_pause_moderate_files) + len(fsm_with_pause_fast_files) + len(fsm_with_pause_moderate_files) + len(fsm_with_pause_slow_files) + len(turnaround_files):
                            random_file = random.choice(turnaround_files)
                            random_file_path = os.path.join(turnaround, random_file)
                            print("Randomly selected turnaround lick file:", random_file_path)
                        else:
                            random_file = random.choice(turnaround_with_pause_files)
                            random_file_path = os.path.join(turnaround_with_pause, random_file)
                            print("Randomly selected turnaround_with_pause lick file:", random_file_path)

                        if random_file_path not in lick_samples:
                            if random_file_path.find("repetition") != -1:
                                At_least_one_repetition = True
                            elif random_file_path.find("turnaround") != -1:
                                At_least_one_turnaround = True
                            
                            lick_samples.append(random_file_path)
                            break
                        else:
                            continue
                else:
                    print("No files found in the folders.")

        q += 1 # Loop control


    classified_licks = []
    # Classify the selected samples
    for lick in lick_samples:
        classified_lick = lick_classification(lick)
        classified_licks.append(classified_lick)

    return classified_licks

#select_N_lick_samples(5)
