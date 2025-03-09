import os
import xml.etree.ElementTree as ET

def post_process(input_files, output_file):
    """
    Merges multiple MusicXML 'score-partwise' files (assuming each has a single <part>)
    in the order given by 'input_files'. The measures from the second file onward are
    appended (with renumbering) to the first file's measures. The merged MusicXML is
    written to 'output_file'.

    :param input_files: List of paths to MusicXML files to be merged
    :param output_file: Path of the merged output file
    """

    if not input_files:
        raise ValueError("No input files provided.")

    # 1) Parse the first file to get the 'base' tree
    base_tree = ET.parse(input_files[0])
    base_root = base_tree.getroot()

    # Locate the single <part> in the first file
    base_part = base_root.find(".//part")
    if base_part is None:
        raise ValueError(f"No <part> found in first file {input_files[0]}")

    # Count how many measures currently in the base file
    measure_offset = len(base_part.findall("measure"))

    # 2) For each subsequent file, parse, renumber, and append
    for musicxml_path in input_files[1:]:
        tree = ET.parse(musicxml_path)
        root = tree.getroot()

        part = root.find(".//part")
        if part is None:
            raise ValueError(f"No <part> found in file {musicxml_path}")

        measures = part.findall("measure")

        # Renumber measures so they continue after the current offset
        for idx, measure in enumerate(measures, start=1):
            measure_number = str(measure_offset + idx)
            measure.set("number", measure_number)

            # Append the measure to the base part
            base_part.append(measure)

        # Update measure offset so the next file's measures start after these
        measure_offset += len(measures)

    # (3) Write out the merged tree to a new file
    # ElementTree does not preserve the DOCTYPE, so it won't appear in the output.
    base_tree.write(output_file, encoding="UTF-8", xml_declaration=True)

    with open(output_file, "w", encoding="UTF-8") as f:
        # Write the xml declaration and doctype manually
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write('<!DOCTYPE score-partwise PUBLIC\n')
        f.write('    "-//Recordare//DTD MusicXML 1.0 Partwise//EN"\n')
        f.write('    "/musicxml/partwise.dtd">\n')

        # Now let ElementTree write out the merged <score-partwise> content
        base_tree.write(f, encoding="unicode", xml_declaration=False)

    return output_file


'''
file_paths_for_the_ordered_licks_in_the_solution = []

for vertex in graph_path_vertices_ordered:
    file_paths_for_the_ordered_licks_in_the_solution.append(licks_list[vertex][-1])

#print(file_paths_for_the_ordered_licks_in_the_solution)
'''    
'''
# Example usage:
files_to_merge = [
    "/home/sergio/Downloads/licks_dataset_sampling/FMS/regular/fast/3.xml",
    "/home/sergio/Downloads/licks_dataset_sampling/turnaround_with_pause/10.xml",
    "/home/sergio/Downloads/licks_dataset_sampling/turnaround/12.xml"
    # ... as many as needed, in the order you want them merged
]
'''
'''
output_file = "ordered_licks_optm_output.xml"

post_process(file_paths_for_the_ordered_licks_in_the_solution, output_file)
print(f"Merged MusicXML written to {output_file}")
'''
