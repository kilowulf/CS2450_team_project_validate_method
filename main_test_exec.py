"""CS 2450 Scrumsters
Duncan DeNiro,
Carston Dastrup
Aaron Brown
Andrew Campbell
"""
import math

"""
opcodes:
                Name   Operator   Operand                   Description
                READ    10        Destination Mem add.      Reads a word into mem location
                WRITE   11        Source Mem add.           Write word from loc. to screen
                LOAD    20        Source Mem add.           load word at mem loc. to Accum.
                STORE   21        Dest. Mem add.            store word from Accum to mem loc.
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
        self.opCode_reg = []
        self.storedOpCodes = []  # list of input opcodes
        self.storedMemory = []  # list of input memory location
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
        print("Accumulator:          " + str(math.floor(self.Accumulator)))
        print("InstructionCounter:  0" + str(self.InstructCounter))
        print("InstructionRegister: 0" + str(self.InstructRegister))
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

    # this will return a string
    def LinePrompt(self):
        # LineNum  requires some class name/required variable to iterate.
        return input("{:02d}?".format(self.LineNum))

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

        # check for none integer input
        if user_input.isalpha():
            self.validate_pass = False
            return print(f'{user_input} please enter integers only'), self.validate_pass

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
        print(
            "*** Please enter your program one instruction ***\n*** ( or data word ) at a time into the input "
            "***\n*** text field. I will display the location ***\n*** number and a question mark (?). You then "
            "***\n*** type the word for that location. Enter ***\n*** -99999 to stop entering your program. ***")
        incoming = None
        inc = 0

        while incoming != "-99999":
            if inc < 10:
                print("0" + str(inc) + " ? ", end="")
            else:
                print(str(inc) + " ? ", end="")

            incoming = input()
            self.validate(incoming)
            if not self.validate_pass:
                self.validate_pass = True
                continue
            inc += 1
            if incoming != "-99999":
                self.InstructCounter += 1
                self.opCode_reg.append(incoming)
                self.opCode = incoming[:2]
                self.operand = incoming[2:]
            self.storedMemory.append(incoming[2:])  # memory list
            self.storedOpCodes.append(incoming[:2])  # opcode list

    def loadingStarting(self):
        print("*** Program loading completed ***\n*** Program execution begins ***")
        count = 0
        for i in self.storedOpCodes:
            if i == "10":  # Read
                word = input("Enter an integer:")
                self.memory[int(self.storedMemory[count])] = int(word)
                self.InstructRegister = self.opCode_reg[-1]
                self.InstructCounter = int(self.storedMemory[count]) + 1
            if i == "11":  # Write
                print(f'WRITE from {self.storedMemory[count]}: {self.memory[int(self.storedMemory[count])]}')
            if i == "20":  # load
                print("Loading from memory to accumulator: ")
                value_to_load = self.memory[int(self.storedMemory[count])]
                self.Accumulator = value_to_load
                self.InstructCounter = int(self.storedMemory[count]) + 1
            if i == "21":  # Store
                value_to_store = self.Accumulator
                self.memory[int(self.storedMemory[count])] = value_to_store
                self.InstructCounter = int(self.storedMemory[count]) + 1
                print(f'STORE {value_to_store} from accumulator to memory loc.: {self.storedMemory[count]}')
            if i == "30":  # Add
                value_to_add = self.memory[int(self.storedMemory[count])]
                self.Accumulator += value_to_add
                self.InstructCounter = int(self.storedMemory[count]) + 1
                print(f'ADD {value_to_add} at mem loc. {int(self.storedMemory[count])} to accumulator: {self.Accumulator}')
            if i == "31":  # Subtract
                # results in a -0000 when accumulator is stored
                value_to_sub = self.memory[int(self.storedMemory[count])]
                self.Accumulator -= value_to_sub
                self.InstructCounter = int(self.storedMemory[count]) + 1
                print(f'SUBTRACT {value_to_sub} at mem loc. {int(self.storedMemory[count])} from accumulator: {self.Accumulator}')
            if i == "32":  # Divide
                value_denominator = self.memory[int(self.storedMemory[count])]
                self.Accumulator = int(math.floor(self.Accumulator / value_denominator))
                self.InstructCounter = int(self.storedMemory[count]) + 1
                print(f'DIVIDE {value_denominator} at mem loc. {int(self.storedMemory[count])} from accumulator: {self.Accumulator}')
            if i == "33":  # Multiply
                value_to_multi = self.memory[int(self.storedMemory[count])]
                self.Accumulator *= value_to_multi
                self.InstructCounter = int(self.storedMemory[count]) + 1
                print(f'MULTIPLY {value_to_multi} at mem loc. {int(self.storedMemory[count])} to accumulator: {int(self.Accumulator)}')
            if i == "40":  # branch
                branch_add = int(self.storedMemory[count])
                self.InstructCounter = branch_add
            if i == "41":  # branching
                branch_add = int(self.storedMemory[count])
                if self.Accumulator < 0:
                    self.InstructCounter = branch_add
            if i == "42":  # branchzero
                branch_add = int(self.storedMemory[count])
                if self.Accumulator == 0:
                    self.InstructCounter = branch_add
            if i == "43":  # halt
                quit()
            count += 1

    # main method if we want it not in a seperate class


def main():
    vm = virtualMachine()
    vm.prompt()
    vm.execute()
    vm.loadingStarting()
    vm.Dump()


if __name__ == "__main__":
    main()
