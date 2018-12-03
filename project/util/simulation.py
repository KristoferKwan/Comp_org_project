""" Authored jointly by the team
    Date: December 2018
"""


def simulate(instruction_list, use_forwarding):
    """ Main simulation loop that outsources instruction printing to the instruction.py
        module.

        :param  instruction_list:   stores Instruction class instances based on the input file.
        :type   instruction_list:   list
        :param  use_forwarding:     specifies whether forwarding should be used in the simulation
        :type   use_forwarding:     boolean
    """

    num_cycles = instruction_list[- 2].cycle_range[1]

    print("START OF SIMULATION " + ("(forwarding)" if use_forwarding else "(no forwarding)"))
    line = "----------------------------------------------------------------------------------"

    for i in range(1, num_cycles):
        print("CPU Cycles ===>\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\t16\n")
        for j in range(0, len(instruction_list)):
            if j > 0 and not instruction_list[j].is_double_dep and i >= instruction_list[j].cycle_range[0] + 2:
                for k in range(0, instruction_list[j].nops_required):
                    instruction_list[-1].cycle_range[0] = instruction_list[j].cycle_range[0]
                    instruction_list[-1].cycle_range[1] = instruction_list[j].cycle_range[1] + 4
                    instruction_list[-1].sim_print(i)
            else:
                instruction_list[j].sim_print(i)
        print(line)

    print("END OF SIMULATION")
