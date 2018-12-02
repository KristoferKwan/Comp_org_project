from project.util import Instruction

if __name__ == "__main__":
    test = Instruction("add $t0,$t1,$t2", "add", 0, 1, 2, 1, 5, 0, 0, False)
    print(test.full)
