""" Author: Peter Gravelin
    Date: 2018 December
"""


class Instruction(object):
    """ Instruction class definition that holds information for the instruction's
    full text, operation, destination register, both source source registers,
    the start and end cycles, the number of nops that must be printed before it,
    the cycle that the instruction should stall until, and whether it is doubly
    dependent with the previous instruction on a particular register.
    """
    def __init__(self, full_instruction, operation, dest_reg, src_reg1, src_reg2, start_cycle,
                 end_cycle, nops_required, stall_until, is_double_dependent):
        self.full = full_instruction
        self.op = operation
        self.dest = dest_reg
        self.src1 = src_reg1
        self.src2 = src_reg2
        self.startCycle = start_cycle
        self.endCycle = end_cycle
        self.nopsRequired = nops_required
        self.stallUntil = stall_until
        self.isDoubleDep = is_double_dependent


def generate_instructions(file):
    """ Generate Instruction class instances based on the input file and return them.

    param   text or assembly file input by the user as a command-line argument
    type    file
    return  list of Instruction class objects
    """
    pass


def print_instruction(instruction):
    """ Print instruction based on its class attributes.

    param   Instruction class instance
    type    Instruction
    """
    pass
