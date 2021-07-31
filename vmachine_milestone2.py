"""CS 2450 Scrumsters
Duncan DeNiro,
Carston Dastrup
Aaron Brown
Andrew Campbell
"""
import ast
import math
from typing import List, Callable
from abc import ABC, abstractmethod

"""
opcodes:
                Name   Operator   Operand                   Description
                READ    10        Destination Mem add.      Reads a word into mem location
                WRITE   11        Source Mem add.           Write word from loc. to screen
                WRITEASCII 12     Source Mem add.           write to output ascii char from src. add.
                LOAD    20        Source Mem add.           load word at mem loc. to Accum.
                STORE   21        Dest. Mem add.            store word from Accum to mem loc.
                SETACCUM 22       Value                     Set value of accumulator.
                ADD     30        Src. Mem add.             add word from mem loc. to value in
                                                            Accum. - result stays in Accum.
                SUBTRACT 31       Src. Mem. add.            SUBTRACT word in mem loc. from word
                                                            in Accum. result stays in Accum.
                DIVIDE  32        Src. Mem. add             DIVIDE word in Accum. by word in
                                                            mem loc. result left in Accum.
                MULTIPLY 33       Src. Mem add              MULTIPLY word in mem loc. by
                                                            word in Accum. result left in Accum.
                BRANCH   40       Branch Mem. Add.          Branch to mem loc.
                BRANCHNEG 41      Branch Mem Add            Branch to Mem. loc if word in Accum.
                                                            is Negative.
                BRANCHZERO 42     Branch Mem. Add.          Branch to mem. loc if word in Accum.
                                                            is zero
                HALT       43     None                      Pause program
"""


class virtualMachine:
    # default constructor
    def __init__(self):
        self.memory = [None] * 100  # list of size 100 filled with zero's
        for i in range(100):
            self.memory[i] = 0
        self.operand = 0
        self.exitCode = -99999
        self.opCode = 0
        self.storedOpCodes = []  # list of input opcodes
        self.storedMemory = []  # list of input memory loccation
        self.validate_pass = True

        self.InstructCounter = 0
        self.InstructRegister = 0
        self.Accumulator = 0
        self.LineNum = 0
        self.LoadDialog = ""

    # This is where our function definitions are

    # logError does not return anything but will post an error log to console, I believe.
    def LogError(self, message):
        print("Returns nothing")

    # Dump, display all whats stored in memory
    def Dump(self):
        print("\nREGISTERS:          ")
        print("Accumulator:          " + str(self.Accumulator))
        print("InstructionCounter:  " + str(self.InstructCounter))
        print("InstructionRegister:  " + str(self.InstructRegister))
        print("OperationCode:        " + str(self.opCode))
        print("Operand:              " + str(self.operand))
        # Below is getting the format of the array displayed
        multiple = 0
        counter = 10
        print("\nMEMORY:")
        print("    00     01     02     03     04     05     06     07     08     09", end="")
        for index in self.memory:
            if counter % 10 == 0:
                print("\n" + str(multiple) + "0 ", end=" ")
                multiple += 1
                counter = 0
            counter += 1
            print(f"{index:05d}", end="")  # displaying with leading zeros
            print(" ", end=" ")

    # Calls the prompt to the console. This likely will be called on load.
    # this may return a string?
    def prompt(self):
        print("""

             _   ___   _____ ___ __  __ 
             | | | \ \ / / __|_ _|  \/  |
             | |_| |\ V /\__ \| || |\/| |
             \___/  \_/ |___/___|_|  |_|
                Welcome to UVSim
        This program interprets and runs programs written in the BasicML language.
        Usage: The program is entered line by line. Once your program has been entered enter -99999 to run the application.
        You will be prompted with each line number sequentially followed by ? where you can input your BasicML for that line.
            """)
        print(
            "*** Please enter your program one instruction ***\n*** ( or data word ) at a time into the input ***\n*** text field. I will display the location ***\n*** number and a question mark (?). You then ***\n*** type the word for that location. Enter ***\n*** -99999 to stop entering your program. ***")

    # this will validate input from users
    def validate(self, user_input):
        # Opcodes
        opcodes = [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43]
        # exitcode
        exit_code = str(-99999)

        # check for entry
        if user_input is None:
            self.validate_pass = False
            return print(f'No input detected'), self.validate_pass
            return print(f'No input detected')

        # check for none integer input
        if user_input.isalpha():
            self.validate_pass = False
            return print(f'{user_input} please enter integers only'), self.validate_pass
            return print(f'{user_input} please enter integers only')

        # convert input to string
        input_to_string = str(user_input)
        if input_to_string == exit_code:
            return print(f'exit code')
        # check for input less than 4
        if len(input_to_string) <= 4:
            if len(input_to_string) < 4:
                self.validate_pass = False
                return print(f'{input_to_string} has too few digits')
            if input_to_string[0] == '-':
                self.validate_pass = False
                return print(f'{input_to_string} has too few digits')
        # check to make sure input is either length 5 if signed or 4 if unsigned
        if len(input_to_string) >= 5 and input_to_string != exit_code:
            if len(input_to_string) > 5:
                self.validate_pass = False
                return print(f'{input_to_string} has too many digits')
            if len(input_to_string) == 5 and input_to_string[0] != '-':
                self.validate_pass = False
                return print(f'{input_to_string} must be 4 digits only')
        # check if input is a negative value
        if input_to_string[0] == '-':
            if input_to_string != exit_code:
                # slice opcode as substring
                input_to_string = input_to_string[1:]
                operator = input_to_string[0:2]
                # check opcode
                if int(operator) not in opcodes:
                    self.validate_pass = False
                    return print(f'{user_input} incorrect operator entered')
        input_operator = input_to_string[0:2]
        if int(input_operator) not in opcodes:
            self.validate_pass = False
            return print(f'{user_input} incorrect operator entered')

    def validate_memory(self, curr_mem_len):
        if curr_mem_len > len(self.memory):
            print(f'Memory Exceeded')

    def validate_instruct_counter(self, curr_counter_value):
        if curr_counter_value > len(self.memory):
            print(f'Too many entries have been made')

    # running a while loop getting the first instruction inputs seperating them in their own lists
    def execute(self):
        incoming = None
        inc = 0

        while incoming != "-99999":
            if inc < 10:
                print("0" + str(inc) + " ? ", end="")
            else:
                print(str(inc) + " ? ", end="")

            incoming = input()
            self.validate(incoming)
            if self.validate_pass == False:
                self.validate_pass = True
                continue

            if incoming != "-99999":
                self.InstructCounter += 1
                self.memory[inc] = incoming
                inc += 1
            self.storedMemory.append(incoming[2:])  # memory list
            self.storedOpCodes.append(incoming[:2])  # opcode list

    def loadingStarting(self):
        print("*** Program loading completed ***\n*** Program execution begins ***")
        for opcode in self.memory:
            op = Opcodes()
            op_obj = OpcodeObject(opcode)
            op.opcode_execute(op_obj)

    # main method if we want it not in a seperate class


# basic opcode object
class OpcodeObject:
    operator: str
    operand: str
    opcode_str: str

    def __init__(self, opcode_str):
        self.opcode_str = str(opcode_str)
        self.operator = opcode_str[:2]
        self.operand = opcode_str[2:]


# class inherits from virtual machine to pass to derived classes
class OpcodeOperation(ABC, virtualMachine):

    @abstractmethod
    def operation(self, opcode_obj: OpcodeObject):
        pass


class Opcodes(virtualMachine, OpcodeObject):

    def opcode_find(self, opcode_obj: OpcodeObject):
        opcode_dict = {'10': read(),
                       '11': write(),
                       '12': writeAscii(),
                       '20': load(),
                       '21': store(),
                       '22': setAccum(),
                       '30': add(),
                       '31': subtract(),
                       '32': divide(),
                       '33': multiply(),
                       '40': branch(),
                       '41': branchNeg(),
                       '42': branchZero(),
                       '43': halt()}

        if opcode_obj.operator in opcode_dict:
            operation_class = opcode_dict[opcode_obj.operator]
            return operation_class

    def opcode_execute(self, opcode_obj: OpcodeObject):
        op_class = self.opcode_find(opcode_obj)
        return op_class.operation(opcode_obj)


# i/o
class read(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        operand = opcode_obj.operand
        word = input("Enter a value: ")
        self.memory[int(operand)] = int(word)
        self.InstructRegister = opcode_obj.opcode_str
        self.InstructCounter = self.memory.index(opcode_obj.opcode_str) + 1
        return


class write(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        operand = opcode_obj.operand
        print(f'WRITE from {self.memory[operand]}: {self.memory[int(self.memory[operand])]}')


class writeAscii(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        operand = opcode_obj.operand
        print(f'WRITE from {self.storedMemory[operand]}: {chr(self.memory[int(self.memory[operand])])}')


# load ops
class load(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        operand = opcode_obj.operand
        value_to_load = self.memory[operand]
        self.Accumulator = value_to_load


class store(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        operand = opcode_obj.operand
        value_to_store = self.Accumulator
        self.memory[operand] = value_to_store


class setAccum(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        accum_value = opcode_obj.operand
        self.Accumulator = accum_value


# Arithmetic
class add(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        operand = opcode_obj.operand
        value_to_add = self.memory[int(operand)]
        self.Accumulator += value_to_add  # Use setAccum?
        print(f'ADD {value_to_add} at mem loc. {int(self.memory[operand])} to accumulator: {self.Accumulator}')


class subtract(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        operand = opcode_obj.operand
        value_to_sub = self.memory[int(operand)]
        self.Accumulator = - value_to_sub  # Use setAccum?
        print(f'SUBTRACT {value_to_sub} at mem loc. {int(self.memory[operand])} from accumulator: {self.Accumulator}')


class divide(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        operand = opcode_obj.operand
        value_denominator = self.memory[int(operand)]
        self.Accumulator //= value_denominator
        print(
            f'DIVIDE {value_denominator} at mem loc. {int(self.memory[operand])} from accumulator: {int(self.Accumulator)}')


class multiply(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        operand = opcode_obj.operand
        value_to_multi = self.memory[int(operand)]
        self.Accumulator *= value_to_multi
        print(
            f'MULTIPLY {value_to_multi} at mem loc. {int(self.memory[operand])} to accumulator: {int(self.Accumulator)}')


# Control
class branch(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        branch_address = opcode_obj.operand
        value = self.memory[int(branch_address)]  # if value at address is needed
        self.InstructRegister = opcode_obj.opcode_str
        self.InstructCounter = int(branch_address) + 1
        return


class branchZero(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        branch_address = opcode_obj.operand
        if self.Accumulator == 0:
            self.InstructCounter = int(branch_address)
            self.InstructRegister = opcode_obj.opcode_str
        return


class branchNeg(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        branch_address = opcode_obj.operand
        value = self.memory[int(branch_address)]  # if value at address is needed
        if self.Accumulator < 0:
            self.InstructCounter = int(branch_address)
            self.InstructRegister = opcode_obj.opcode_str


class halt(OpcodeOperation):
    def operation(self, opcode_obj: OpcodeObject):
        quit()


def main():
    vm = virtualMachine()
    vm.prompt()
    vm.execute()
    vm.loadingStarting()
    vm.Dump()


if __name__ == "__main__":
    main()
