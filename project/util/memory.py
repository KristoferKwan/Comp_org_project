""" Author: Kristofer Kwan
    Date: 2018 December
"""

class Memory(object):
	def __init__(self): #initializes the memory list (which is a dictionary 
						#of all the registers as keys and the stored value of that register as the value)
		memory_list = dict()
		for i in range(8):
			memory_list['$s'+str(i)] = 0
		for i in range(10):
			memory_list['$t'+str(i)] = 0
		self.memory_list = memory_list
	
	def __str__(self):	#printing the memory in the right format
		mem_sort = list(self.memory_list.keys())
		mem_sort.sort()	#create a list and sorts it so that the order of the registers is maintained
		k_index = 0
		mem = ""
		for key in mem_sort:
			k_index+=1
			mem += key + " = " + str(self.memory_list[key]) 
			if k_index % 4 == 0:
				mem += "\n"
			else:
				mem += "\t\t"
		return mem

	def	get_memory_list(self):	#returns the memory_list referenced
		return self.memory_list


	def evaluate_line(self, curr_line):
		if len(curr_line.registers) == 3:
			if curr_line.operation == "add":
				self.memory_list['$'+curr_line.registers[0]] = self.memory_list['$'+curr_line.registers[1]] + \
				self.memory_list['$'+curr_line.registers[2]]
			elif curr_line.operation == "sub":
				self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] - \
				self.memory_list['$' + curr_line.registers[2]]
			elif curr_line.operation == "and":
				self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] & \
				self.memory_list['$' + curr_line.registers[2]]
			elif curr_line.operation == "or":
				self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] | \
				self.memory_list['$' + curr_line.registers[2]]
			elif curr_line.operation == "slt":
				self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] | \
				self.memory_list['$' + curr_line.registers[2]]
		else:
			if curr_line.operation == "addi":
				self.memory_list['$'+curr_line.registers[0]] = self.memory_list['$'+curr_line.registers[1]] + \
				self.memory_list['$'+curr_line.registers[2]]
			elif curr_line.operation == "subi":
				self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] - \
				self.memory_list['$' + curr_line.registers[2]]
			elif curr_line.operation == "andi":
				self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] & \
				self.memory_list['$' + curr_line.registers[2]]
			elif curr_line.operation == "ori":
				self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] | \
				self.memory_list['$' + curr_line.registers[2]]
			elif curr_line.operation == "slti":
				self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] | \
				self.memory_list['$' + curr_line.registers[2]]

		return

#I used the following to test the memory ==> look below to see how assignments are done
# Memory = Memory()
# a_test = Memory.get_memory_list()


# a_test['$s3'] = a_test['$s1']
# a_test['$s3'] = 3
# print(Memory)
