""" Authored jointly by the team
    Date: December 2018
"""
import copy

def print_list(instr_list):
    for item in instr_list:
        item.debug_print()
    print()

def loop(branch_instr, instr_list):
    #need instr_list to determine the instructions after current
    #in the last loop iteration, the stalls for instructions past bne and beq are removed. 
    stages = ["IF", "ID", "EX", "MEM", "WB", "*"]
    loop_indx = branch_instr.branch_range[0] 
    loop_end = branch_instr.branch_range[1]
    num_affected = min(4 + loop_end, len(instr_list))
    stall_size = num_affected - loop_end            #   how many instructions are being stalled after the end of the loop(bne and beq)
    loop_and_stall_size = num_affected - loop_indx  #   how many instructions between the start of the loop branch to the last stalled instruction
    looped_inst = []
    
    for i in range(loop_indx, num_affected):
        distance_from_stall = i - loop_indx        #   distance from the last stalled instruction   
        instr_cpy = copy.deepcopy(instr_list[i])
        if(instr_cpy.operation == "bne" or instr_cpy.operation == "beq"):
            instr_cpy.branch_range[0] += loop_and_stall_size 
            instr_cpy.branch_range[1] += loop_and_stall_size
        #print("This is the cycle range: {:d} - {:d}".format(branch_instr.cycle_range[0], branch_instr.cycle_range[1]))
        instr_cpy.cycle_range[0] = branch_instr.cycle_range[0] + distance_from_stall + stall_size   #   changing the start index and the end index start and end cycles
        instr_cpy.cycle_range[1] = branch_instr.cycle_range[1] + distance_from_stall + stall_size   #   changing the start index and the end index start and end cycles
        instr_cpy.is_evaluated = False
        looped_inst.append(instr_cpy)

    for i in range(loop_end + 1, num_affected):
        instr_list[i].stages = stages[: 5 -  (i - loop_end + 1)] + ["*"] * ((i - loop_end) + 1)

    nop = instr_list[-1]
    instr_list = (instr_list[0: -1] + looped_inst)
    instr_list.append(nop)
    # print_list(instr_list)
    return instr_list

def simulate(instruction_list, use_forwarding, memory):
    """ Main simulation loop that outsources instruction printing to the instruction.py
        module.

        :param  instruction_list:   stores Instruction class instances based on the input file.
        :type   instruction_list:   list
        :param  use_forwarding:     specifies whether forwarding should be used in the simulation
        :type   use_forwarding:     boolean
    """
    num_instructions_fetched = 1
    i = 0
    line = "----------------------------------------------------------------------------------"
    print("START OF SIMULATION " + ("(forwarding)" if use_forwarding == "F" else "(no forwarding)") + "\n" + line)

    while i <= 16 and i+1 <= instruction_list[-2].cycle_range[1]:
        i += 1
        print("CPU Cycles ===>     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16")
        j = 0
        while j < num_instructions_fetched:
            if j > 0 and not instruction_list[j].is_double_dep and i >= instruction_list[j].cycle_range[0] + 2:
                for k in range(0, instruction_list[j].nops_required):       #stall
                    instruction_list[-1].cycle_range[0] = instruction_list[j].cycle_range[0]
                    instruction_list[-1].cycle_range[1] = instruction_list[j].cycle_range[0] + 4
                    instruction_list[-1].sim_print(i, memory)
            instruction_list[j].sim_print(i, memory)
            if instruction_list[j].operation == "bne" or instruction_list[j].operation == "beq":
                if instruction_list[j].should_branch:
                    instruction_list = loop(instruction_list[j], instruction_list)
                    num_cycles = instruction_list[-2].cycle_range[0]
                    instruction_list[j].should_branch = False
            j += 1
        if num_instructions_fetched != len(instruction_list) - 1:
            num_instructions_fetched += 1
        print("")
        print(memory)
        print(line)
        if num_instructions_fetched > 16:
            break
    print("END OF SIMULATION")
