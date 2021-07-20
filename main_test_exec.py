"""CS 2450 Scrumsters
Duncan DeNiro,
Carston Dastrup
Aaron Brown
Andrew Campbell
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
        self.pass_validate = True
        self.storedOpCodes = []
        self.storedMemory = []

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
        if self.exitCode:
            print("\nREGISTERS:          ")
            print("Accumulator:          " + str(self.Accumulator))
            print("InstrucctionCounter:  " + str(self.InstructCounter))
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

            print(f'store memory for data {self.storedMemory}')
            print(f'stored memory for opcodes {self.storedOpCodes}')

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
        exit_code = str(self.exitCode)

        # check for entry
        if user_input is None:
            self.pass_validate = False
            return print(f'No input detected')

        # check for none integer input
        if not isinstance(user_input, int):
            self.pass_validate = False
            return print(f'{user_input} please enter integers only')

        # convert input to string
        input_to_string = str(user_input)

        if input_to_string == exit_code:
            self.pass_validate = False
            return print(f'exit code')

        # check for input less than 4
        if len(input_to_string) <= 4:
            if len(input_to_string) < 4:
                self.pass_validate = False
                return print(f'{input_to_string} has too few digits')

            if input_to_string[0] == '-':
                self.pass_validate = False
                return print(f'{input_to_string} has too few digits')

        # check to make sure input is either length 5 if signed or 4 if unsigned
        if len(input_to_string) >= 5 and input_to_string != exit_code:
            if len(input_to_string) > 5:
                self.pass_validate = False
                return print(f'{input_to_string} has too many digits')

            if len(input_to_string) == 5 and input_to_string[0] != '-':
                self.pass_validate = False
                return print(f'{input_to_string} must be 4 digits only')

        # check if input is a negative value
        if input_to_string[0] == '-':
            if input_to_string != exit_code:
                # slice opcode as substring
                input_to_string = input_to_string[1:]
                operator = input_to_string[0:2]

                # check opcode
                if int(operator) not in opcodes:
                    self.pass_validate = False
                    return print(f'{user_input} incorrect operator entered')

        input_operator = input_to_string[0:2]
        if int(input_operator) not in opcodes:
            self.pass_validate = False
            return print(f'{user_input} incorrect operator entered')

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
            self.validate(int(incoming))
            # if validation fails then break out of loop
            if not self.pass_validate:
                break
            else:
                inc += 1
                # slice substring to consider negative values
                if incoming[0] == '-':
                    inc_operand = incoming[3:]
                    inc_operator = incoming[1:3]
                    # re-introduce negative sign for negative values in memory
                    self.storedMemory.append('-' + inc_operand)  # memory list
                    self.storedOpCodes.append(inc_operator)  # opcode list
                else:
                    inc_operand = incoming[2:]
                    inc_operator = incoming[0:2]
                    self.storedMemory.append(inc_operand)  # memory list
                    self.storedOpCodes.append(inc_operator)  # opcode list



    # main method if we want it not in a seperate class


def main():
    vm = virtualMachine()

    vm.prompt()
    vm.execute()
    # user_input_value = -1011
    # user_input_string = str(user_input_value)
    # if user_input_string[0] == '-':
    #     user_input_string = user_input_string[1:3]
    #
    # vm.validate(user_input_string)
    # # use pass_validate to check if validation passes
    # if not vm.pass_validate:
    #     print('Validation failed')

    # vm.Dump()


if __name__ == "__main__":
    main()