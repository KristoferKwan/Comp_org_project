""" Author: Peter Gravelin
    Date: December 2018
"""


def usage():
    """ Warning function for command-line input outputs a demand for the run.py file,
        a forwarding or no forwarding specifier, and a valid input file to be
        written by the user.
    """
    print("You must enter exactly 3 command line inputs")
    print("+------------------------------------------+")
    print("1. The python executable, run.py\n"
          "2. F/N to specify forwarding or no forwarding\n"
          "3. A valid input file (*.txt)\n")
    print("USAGE: ./python run.py {F,N} {*.txt}")
