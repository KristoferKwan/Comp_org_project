""" Author: Peter Gravelin
    Date: December 2018
"""

from sys import argv, exit
from project.util import simulate, generate_instructions, usage

if __name__ == "__main__":
    """ Main function that outsources instruction generation and the simulation loop 
        to the instruction.py and simulation.py modules.
    """
    if len(argv) != 3 or not argv[1] in ['F', 'N']:
        usage()
        exit(1)
    try:
        with open(argv[2], 'r') as file:
            instructionList = generate_instructions(file)
            useForwarding = True if argv[1] == 'F' else False
            simulate(instructionList, useForwarding)
    except IOError as e:
        usage()
        exit(1)

