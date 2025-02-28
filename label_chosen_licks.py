from lxml import etree

# Extract information from each lick and classify it from C1 to C9
# ------------------------------------------------------------------------------
# Otain first and last notes
tree = etree.parse(r"C:\Users\pc\Documents\TCC_I_dset\licks_dset_new\Turnaround_regular\1.xml")
root = tree.getroot()

# Find all <note> elements
notes = root.findall(".//note")

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
        return "Rest w/ " + duration + " beats duration"

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

lick_1 = [first_note, last_note]
# ------------------------------------------------------------------------------
# Classify it from C1 to C9

# C1 (Repetition)


# C2 (EwP <= 1)
if last_note[0] == "R" and int(last_note[8]) <= 1:
    print("EwP <= 1")

# C3 (EwP > 1)
if last_note[0] == "R" and int(last_note[8]) > 1:
    print("EwP > 1")

# C4 (Ewp > 2)    
if last_note[0] == "R" and int(last_note[8]) > 2:
    print("EwP > 2")

# C5 (SwP)
if first_note[0] == "R":
    print("SwP")

# C6 (SwP > 1)
if first_note[0] == "R" and int(first_note[8]) > 1:
    print("SwP > 1")

# C7 (SwP > 2)
if first_note[0] == "R" and int(first_note[8]) > 2:
    print("SwP > 2")

# C8 (Turnaround)
