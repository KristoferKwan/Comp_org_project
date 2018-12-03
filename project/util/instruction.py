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
        self.cycle_range = [start_cycle, end_cycle]
        self.nops_required = nops_required
        self.stall_until = stall_until
        self.is_double_dep = is_dbl_dependent

    def print_itself(self, current_cycle):
        """ Print instruction based on its class attributes.

            param   Instruction class instance
            param   current cycle of the simulation
            type    Instruction
            type    int
        """
        print(self.full)
        if current_cycle < self.cycle_range[0]:
            print(".\t.\t.\t.\t.\t.\t.\t.\t.")
            return

        stages = ["IF", "ID", "EX", "MEM", "WB", "*"]
        stage = 0

        for i in range(1, 17):
            if current_cycle >= i < self.cycle_range[0] and i <= self.cycle_range[1]:
                if self.operation == "nop":
                    determinate = i - self.cycle_range[0]
                    if determinate >= 2:
                        print(stages[5], end='')
                    else:
                        print(stages[determinate])
                    if i != 16:
                        print('\t', end='')
                else:
                    print(stages[stage])
                    if (stage == 0 and self.nops_required == 2) or \
                            (stage == 0 and self.nops_required == 1 and self.is_double_dep) or \
                            i >= self.stall_until:
                        stage += 1
                    if i != 16:
                        print('\t', end='')
            elif i != 16:
                print('.\t', end='')
            else:
                print('.', end='')
        print('')


def generate_instructions(file):
    """ Generate Instruction class instances based on the input file and return them.

        param   text or assembly file input by the user as a command-line argument
        type    file
        return  list of Instruction class objects
    """
    print("Got to generate")
    instructions = []
    current_cycle = 1

    for line in file:
        instruction = Instruction(line, line[0:line.find(" ")], [current_cycle, current_cycle + 4], 0, 0, False)

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

        for i in range(max(len(instructions) - 2, 0), len(instructions)):
            if (instruction.operation == "sw" and instructions[i].registers[0] == instruction.registers[0]) \
                    or instructions[i].registers[0] in instruction.registers[1:]:
                distance = current_cycle - instructions[i].cycle_range[0]
                instruction.nops_required = distance
                instruction.stall_until = instructions[i].cycle_range[1]
                instruction.cycle_range[1] = instruction.stall_until + 3

        if len(instructions) > 0 and instructions[len(instructions) - 1].nops_required == 2 \
                and instruction.nops_required == 1:
            instruction.cycle_range[1] += 1
            instruction.is_double_dep = True

        instructions.append(instruction)
        current_cycle += 1

    instructions.append(Instruction("nop\t", "nop", [], -1, -1, 0, 0, False))
    return instructions
