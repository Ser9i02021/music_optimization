from label_chosen_licks import select_N_lick_samples
from cost_matrix_construction import build_cost_matrix
from optimization import optimize
from post_processing import post_process


def main():

    # (1) Data Input
    # (2) Selection of Subset of Licks
    licks_list = select_N_lick_samples(32) # Select 30 random licks plus inital and final dummy licks
    
    # (3) Calculation of Cost Matrix
    p = build_cost_matrix(licks_list) # Build the cost matrix

    # (4) Optimization
    file_paths_for_the_ordered_licks_in_the_solution = optimize(licks_list, p, 11)

    # (5) Postprocessing
    # (6) Export as MusicXML
    output_file = "ordered_licks_optm_output.xml"
    XML_optm_licks_file = post_process(file_paths_for_the_ordered_licks_in_the_solution, output_file)

    print(f"Merged MusicXML written to {XML_optm_licks_file}")

if __name__ == "__main__":
    main()