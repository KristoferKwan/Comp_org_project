""" Authored jointly by the team
    Date: December 2018
"""
from .memory import Memory
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
    #print("loop_indx =", loop_indx)
    #print("loop_end =", loop_end)
    num_affected = min(4 + loop_end, len(instr_list))

    looped_inst = []
    for i in range(loop_indx, num_affected):
        instr_cpy = copy.deepcopy(instr_list[i])
        instr_cpy.cycle_range[0] = branch_instr.cycle_range[0] + i + num_affected - loop_end - 1 #changing the start index and the end index start and end cycles
        instr_cpy.cycle_range[1] = branch_instr.cycle_range[1] + i + num_affected - loop_end - 1 #changing the start index and the end index start and end cycles 
        if(instr_cpy.operation == "bne" or instr_cpy.operation == "beq"):
            instr_cpy.branch_range[0] += loop_end - loop_indx  
            instr_cpy.branch_range[1] += loop_end - loop_indx  
        looped_inst.append(instr_cpy)

    for i in range(loop_end + 1, num_affected):
        instr_list[i].stages = stages[: 5 -  (i - loop_end + 1)] + ["*"] * ((i - loop_end) + 1)
        # instr_list[i].stages += stages[5] * (6 - curr_stage)
        #this is to take the instructions and change stage accordingly
        #print("PRINT")
        #print("{:s}: instr_list[i].stages".format(instr_list[i].operation), instr_list[i].stages)
    #print_list(instr_list)
    nop = instr_list[-1]
    instr_list = (instr_list[0: -1] + looped_inst)
    instr_list.append(nop)
    return instr_list
    #you will need to change the cycle range 

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
    num_cycles = instruction_list[-2].cycle_range[0]
    line = "----------------------------------------------------------------------------------"
    print("START OF SIMULATION " + ("(forwarding)" if use_forwarding == "F" else "(no forwarding)") + "\n" + line)

    while(i <= 16 and i+1 <= instruction_list[-2].cycle_range[1]):
        i += 1
        print("CPU Cycles ===>\t\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\t16")
        for j in range(0, num_instructions_fetched):
            if j > 0 and not instruction_list[j].is_double_dep and i >= instruction_list[j].cycle_range[0] + 2:
                for k in range(0, instruction_list[j].nops_required):       #stall
                    instruction_list[-1].cycle_range[0] = instruction_list[j].cycle_range[0]
                    instruction_list[-1].cycle_range[1] = instruction_list[j].cycle_range[0] + 4
                    instruction_list[-1].sim_print(i, memory)
            if((instruction_list[j].operation == "bne" or instruction_list[j].operation == "beq")):
                if instruction_list[j].should_branch == True:
                    instruction_list = loop(instruction_list[j], instruction_list)
                    num_cycles = instruction_list[-2].cycle_range[0]
                    instruction_list[j].should_branch = False
            instruction_list[j].sim_print(i, memory)
        if num_instructions_fetched != len(instruction_list) - 1:
            num_instructions_fetched += 1
        print("")
        print(memory)
        print(line)
        #print("{:d}  != {:d}".format( num_instructions_fetched, len(instruction_list) - 1))
    print("END OF SIMULATION")
