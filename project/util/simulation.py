""" Authored jointly by the team
    Date: December 2018
"""

from project.util import Instruction


def simulate(instruction_list, use_forwarding):
    """ Main simulation loop that outsources instruction printing to the instruction.py
        module.

        param   stores Instruction class instances based on the input file.
        param   specifies whether forwarding should be used in the simulation
        type    list
        type    boolean
    """
    print("START OF SIMULATION " + ("(forwarding)" if use_forwarding else "(no forwarding)"))
    print("----------------------------------------------------------------------------------")
    print("END OF SIMULATION")
