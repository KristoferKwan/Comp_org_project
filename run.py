""" Author: Peter Gravelin
    Date: December 2018
"""

from sys import argv, exit
from project.util import simulate, generate_instructions, usage, debug_print_instruction_list, Memory

if __name__ == "__main__":
    """ Main function that outsources instruction generation and the simulation loop 
        to the instruction.py and simulation.py modules.
    """
    if len(argv) != 3 or not argv[1] in ['F', 'N']:
        usage()
        exit(1)
    try:
        with open(argv[2], 'r') as file:
            forwarding = argv[1]
            instruction_list = generate_instructions(file, forwarding)
            memory = Memory()
            debug_print_instruction_list(instruction_list)
            # uncomment to run simulation
            simulate(instruction_list, forwarding, memory)
            #simulate(instruction_list, use_forwarding)

    except IOError as e:
        usage()
        exit(1)

