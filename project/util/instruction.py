class Instruction(object):
    def __init__(self, fullInstruction, operation, destReg, srcReg1, srcReg2, startCycle,
            endCycle, nopsRequired, stallUntil, isDoubleDependent):
        self.full = fullInstruction
        self.op = operation
        self.dest = destReg
        self.src1 = srcReg1
        self.src2 = srcReg2
        self.startCycle = startCycle
        self.endCycle = endCycle
        self.nopsRequired = nopsRequired
        self.stallUntil = stallUntil
        self.isDoubleDep = isDoubleDependent


def generate_instructions():
    pass


def print_instruction():
    pass
