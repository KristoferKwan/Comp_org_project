""" Author: Peter Gravelin
    Date: 2018 December
"""


class Instruction(object):
    """ Instruction class definition that holds information for the instruction's
        full text, operation, destination register, both source source registers,
        the start and end cycles, the number of nops that must be printed before it,
        the cycle that the instruction should stall until, and whether it is doubly
        dependent with the previous instruction on a particular register.

        Contains a function for printing its data.
    """
    def __init__(self, full_instruction="", operation="", registers=[], start_cycle=0, end_cycle=0,
                 nops_required=0, stall_until=0, is_dbl_dependent=False):
        self.full = full_instruction
        self.operation = operation
        self.registers = registers
        self.cycleRange = [start_cycle, end_cycle]
        self.nopsRequired = nops_required
        self.stallUntil = stall_until
        self.isDoubleDep = is_dbl_dependent

    def print(self, current_cycle):
        """ Print instruction based on its class attributes.

            param   Instruction class instance
            param   current cycle of the simulation
            type    Instruction
            type    int
        """
        print(self.full)
        if current_cycle < self.cycleRange[0]:
            print(".\t.\t.\t.\t.\t.\t.\t.\t.")
            return

        # stage = 0

        for i in range(1, 17):
            pass


def generate_instructions(file):
    """ Generate Instruction class instances based on the input file and return them.

        param   text or assembly file input by the user as a command-line argument
        type    file
        return  list of Instruction class objects
    """
    instructions = []
    currentCycle = 1

    for line in file:
        instruction = Instruction(line, [], currentCycle, currentCycle + 4, 0, 0, False)
        instruction.operation = line[0:line.find(" ")]

        reg1 = line.find("$")
        temp = line[reg1 + 1:]
        reg2 = temp.find("$")

        if instruction.operation == "sw":
            instruction.registers.append(reg2)
            instruction.registers.append(reg1)
        else:
            instruction.registers.append(reg1)
            instruction.registers.append(reg2)

            temp = line[reg2 + 1:]
            reg3 = temp.find("$")

            if reg3 != -1:
                instruction.registers.append(reg3)

        for i in range(min(len(instructions) - 2, 0), len(instructions)):
            if (instruction.operation == "sw" and instructions[i].registers[0]
                    == instruction.registers[0]) or instructions[i].registers[0] \
                    in instruction.registers[1:]:
                distance = currentCycle - instructions[i].startCycle
                instruction.nopsRequired = distance
                instruction.stallUntil = instruction[i].endCycle
                instruction.cycleRange[1] = instruction.stallUntil + 3

        if instructions[len(instructions) - 1].nopsRequired == 2 and \
                instruction.nopsRequired == 1:
            instruction.cycleRange[1] += 1
            instruction.isDoubleDep = True

        instructions.append(instruction)

    instructions.append(Instruction("nop\t", "nop", [], -1, -1, 0, 0, False))
    return instructions
