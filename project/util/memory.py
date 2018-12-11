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
		memory_list['$zero'] = 0
		self.memory_list = memory_list
	
	def __str__(self):	#printing the memory in the right format
		mem_sort = list(self.memory_list.keys())
		mem_sort.sort()	#create a list and sorts it so that the order of the registers is maintained
		k_index = 0
		mem = ""
		for key in mem_sort:
			if key == "$zero":
				continue
			k_index+=1
			mem += key + " = " + str(self.memory_list[key]) 
			if k_index % 4 == 0:
				mem += "\n"
			elif int(self.memory_list[key] / 10) <= 0:
				mem += "\t\t"
			else:
				mem += "\t"
		return mem

	def	get_memory_list(self):	#returns the memory_list referenced
		return self.memory_list


	def evaluate_line(self, curr_line):
		if curr_line.operation in ["lw", "sw"]:
			return
		second_operand = curr_line.registers[1]
		if not curr_line.operation in ["beq", "bne"]:
			second_operand = int(curr_line.registers[2]) if type(curr_line.registers[2]) is int \
			else self.memory_list['$' + str(curr_line.registers[2])]

		if curr_line.operation == "add":
			self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] + \
			 second_operand
		elif curr_line.operation == "sub":
			self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] - \
		 	second_operand
		elif curr_line.operation == "and":
			self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] & \
		 	second_operand
		elif curr_line.operation == "or":
			self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[2]] | \
			 second_operand
		elif curr_line.operation == "slt":
			if 0 < self.memory_list['$' + curr_line.registers[2]]:
				self.memory_list['$' + curr_line.registers[0]] = 1
			else:
				self.memory_list['$' + curr_line.registers[0]] = 0
		elif curr_line.operation == "addi":
			self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] + \
			second_operand
		elif curr_line.operation == "subi":
			self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] - \
			second_operand
		elif curr_line.operation == "andi":
			self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] & \
			 second_operand
		elif curr_line.operation == "ori":
			self.memory_list['$' + curr_line.registers[0]] = self.memory_list['$' + curr_line.registers[1]] | \
			 second_operand
		elif curr_line.operation == "slti":
			if self.memory_list['$' + curr_line.registers[1]] < int(curr_line.registers[2]):
				self.memory_list['$' + curr_line.registers[0]] = 1
			else:
				self.memory_list['$' + curr_line.registers[0]] = 0
		elif curr_line.operation == "beq":
			self.memory_list['$' + curr_line.registers[0]] = 1 if self.memory_list['$' + curr_line.registers[1]] == \
															 second_operand else 0
		elif curr_line.operation == "bne":
			self.memory_list['$' + curr_line.registers[0]] = 1 if self.memory_list['$' + curr_line.registers[1]] != \
															 second_operand else 0

#I used the following to test the memory ==> look below to see how assignments are done
# Memory = Memory()
# a_test = Memory.get_memory_list()


# a_test['$s3'] = a_test['$s1']
# a_test['$s3'] = 3
# print(Memory)
