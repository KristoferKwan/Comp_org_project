""" Author: Peter Gravelin
    Date: 2018 December
"""
def print_list(instr_list):
    for item in instr_list:
        item.debug_print()
    print()

class Instruction(object):
    """ Instruction class definition that holds information for the instruction's
        full text, operation, destination register, both source source registers,
        the start and end cycles, the number of nops that must be printed before it,
        the cycle that the instruction should stall until, and whether it is doubly
        dependent with the previous instruction on a particular register.

        Contains a function for printing its data.
    """
    def __init__(self, full_instruction="", operation="", registers=None, start_cycle=0, end_cycle=0,
                 nops_required=0, stall_until=0, is_dbl_dependent=False, should_branch=False, offset=0, is_evaluated = False):
        self.full = full_instruction
        self.operation = operation
        self.registers = [] if registers is None else registers
        self.cycle_range = [start_cycle, end_cycle]
        self.nops_required = nops_required
        self.stall_until = stall_until
        self.is_double_dep = is_dbl_dependent
        self.should_branch = should_branch
        self.offset_index = offset
        self.stages = []
        self.branch_range = []
        self.is_evaluated = is_evaluated

    def __str__(self):
        return self.full

    def debug_print(self):
        """ Print instruction based on its class attributes in debug format.

            :param  self:   current instruction object
            :type   self:   Instruction
        """
        print(self.full)
        print("Operation: " + str(self.operation))
        print("Registers: " + str(self.registers))
        print("Cycle Range: " + str(self.cycle_range))
        print("Nops Required: " + str(self.nops_required))
        print("Stall until cycle: " + str(self.stall_until))
        print("Double Dependent? " + str(self.is_double_dep))
        print("Stall Stages:", self.stages)
        print("Branch Range: " + str(self.branch_range) + "\n")

    def sim_print(self, current_cycle, memory):
        """ Print instruction based on its class attributes in simulation format.

            :param  self:               current instruction object
            :type   self:               Instruction
            :param  int current_cycle:  current simulation cycle
        """


        print(self.full.strip().ljust(20, ' '), end='')
        empty_cycle = ".".ljust(4, ' ')
        if current_cycle < self.cycle_range[0]:
            
            print(empty_cycle * 15 + ".\n", end='')
            return

        if len(self.stages) != 0:
            stages = self.stages
        else:
            stages = ["IF", "ID", "EX", "MEM", "WB", "*"]
        stage = 0

        for i in range(1, 17):
            # Only print the stages of an instruction if current_cycle is within the range of
            # an instruction's cycle_range
            if current_cycle >= i >= self.cycle_range[0] and i <= self.cycle_range[1]:
                if self.operation == "nop":
                    determinate = i - self.cycle_range[0]
                    if determinate >= 2:
                        print(str(stages[5]).ljust(4, ' '), end='')
                    elif i != 16:
                        print(str(stages[determinate]).ljust(4, ' '), end='')
                    else:
                        print(str(stages[determinate]), end='')
                else:
                    # perform logic associated with current stage
                    if i != 16:
                        print(str(stages[stage]).ljust(4, ' '), end='')
                    else:
                        print(str(stages[stage]), end='')
                    if stage == 3 and self.operation in ["bne", "beq"] and not self.is_evaluated:
                        memory.evaluate_line(self)
                        self.is_evaluated = True
                    elif stage == 4 and not self.is_evaluated and stages[4] != "*":
                        memory.evaluate_line(self)
                        self.is_evaluated = True
                    # increment to next stage if as necessary
                    if (stage == 0 and self.nops_required == 2) or \
                            (stage == 0 and self.nops_required == 1 and not self.is_double_dep) or \
                            i >= self.stall_until:
                        stage += 1
                    # if i != 16:
                    #     print(' ' * 4, end='')
            elif i != 16:
                print(empty_cycle, end='')
            else:
                print('.', end='')
        print('')


def debug_print_instruction_list(instruction_list):
    """ Print list of instructions based on Instruction class attributes in debug format.

    :param  instruction_list:   list of Instruction class objects
    :type   instruction_list:   list
    """
    for instruction in instruction_list:
        instruction.debug_print()

def forwarding(curr_instr, previous_instr, distance):
    if previous_instr.operation == 'sw' or previous_instr.operation == 'lw' and \
            distance == 1:
        curr_instr.nops_required = distance
        curr_instr.stall_until = previous_instr.cycle_range[1] - 1
        curr_instr.cycle_range[1] = curr_instr.stall_until + 3

def generate_instructions(file, fwd):
    """ Generate Instruction class instances based on the input file and return them.

        :param      file:   text or assembly file input by the user as a command-line argument
        :type       file:   file
        :param      fwd:    specifies whether or not to apply forwarding
        :type       fwd:    string
        :return:            list of Instruction class objects
        :rtype              list
    """

    labels = dict()
    instructions = []
    current_cycle = 1
    instruction_count = 0
    branch = 1
    stalled = -1
    label = dict()
    for line in file:
        line = line.replace("\n", "")
        if line.find(":") != -1:
            # associate label with the next instruction, works because len(instructions) corresponds to the index
            # of the next instruction to be appended to the list
            labels[line[:-1]] = len(instructions)
            continue

        # fixme: stall_until values may not change (untested)
        instruction = Instruction(line, line[0:line.find(" ")], [],
                                  current_cycle, current_cycle + 4, 0, 0, False, False, 0)

        reg1 = line.find("$")
        reg1_end = line.find(",")
        temp = line[reg1_end + 1:]
        reg2 = temp.find("$")
        reg2_end = temp.find(",")

        # fixme: incorrect registers being appended
        """
        fixes:
        1.Ensured that reg1 and reg2 were not -1 before appending.
        2..find() is called on temp string therefore slicing must be done on temp string
        and not the line string
        3.Created new variable reg_end as an ending constraint of registers in the strings.
        Necessary due to registers having inconsistent string length. e.g. $t1,$zero
        """

        if instruction.operation == "sw":
            if reg2 != -1:
                instruction.registers.append(temp[reg2 + 1:reg2_end])
            if reg1 != -1:
                instruction.registers.append(line[reg1 + 1:reg1_end-1])
        else:
            if reg1 != -1:
                instruction.registers.append(line[reg1 + 1:reg1_end])
            if reg2 != -1:
                end_index = reg2_end if not instruction.operation == "lw" else reg2_end - 1
                instruction.registers.append(temp[reg2 + 1:end_index])

            if instruction.operation == "beq" or instruction.operation == "bne":
                instruction.offset_index = labels[temp[reg2_end + 1:]]
                instruction.branch_range.append(instruction.offset_index)
                instruction.branch_range.append(instruction_count)
            elif instruction.operation != "lw":
                temp = temp[reg2_end + 1:]
                reg3 = temp.find("$")

                #each line has at least two commas. This if statements starts by checking if there is a third.
                if reg2_end != -1 and reg3 != -1: #formerly if reg3 != -1.
                    instruction.registers.append(temp[reg3 + 1: reg3 + 3])
                elif reg3 == -1:
                    num = temp.find(",")
                    instruction.registers.append(int(temp[num + 1:]))

        if fwd != 'F':
            if  stalled != -1:  #will only try to stall if the index is greater than where it was initially stalled        distance = current_cycle - stall_instr.cycle_range[0]
                instruction.stall_until = stall_instr.cycle_range[1] - 1 \
                    if stall_instr.operation in ["sw", "lw"] else stall_instr.cycle_range[1]
                instruction.cycle_range[1] = instruction.stall_until + 3 + start_stall
                start_stall += 1
                if instructions[i].stall_until == current_cycle:
                    stalled = -1

            for i in range(max(len(instructions) - 2, 0), len(instructions)):

                if (instruction.operation == "sw" and instructions[i].registers[0] == instruction.registers[0]) \
                        or instructions[i].registers[0] in instruction.registers[1:]:
                    distance = current_cycle - instructions[i].cycle_range[0]
                    instruction.nops_required = 2 if distance == 1 else 1
                    instruction.stall_until = instructions[i].cycle_range[1] - 1 \
                        if instructions[i].operation in ["sw", "lw"] else instructions[i].cycle_range[1]
                    instruction.cycle_range[1] = instruction.stall_until + 3
                    stall_instr = instructions[i]
                    stalled = i
                    start_stall = 1

            if len(instructions) > 0 and instructions[len(instructions) - 1].nops_required == 2 \
                    and instruction.nops_required == 1:
                instruction.cycle_range[1] += 1
                instruction.is_double_dep = True
        if fwd == 'F' and len(instructions) != 0:
            forwarding(instruction, instructions[len(instructions)-1], current_cycle - instructions[len(instructions)-1].cycle_range[0])
        instructions.append(instruction)
        current_cycle += 1
        instruction_count += 1
    instructions.append(Instruction("nop\t", "nop", [], -1, -1, 0, 0, False))
    return instructions
