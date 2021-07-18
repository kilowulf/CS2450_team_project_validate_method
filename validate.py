""" CS 2450 - Team Project:
    07-10-21
    Aaron Brown
        validate method:
                - test for None: no entry made
                - test for data types: int only
                - test for signed integer to extract operator code properly

"""
global validate_pass
validate_pass = True


def validate(user_input):
    # Opcodes
    opcodes = [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43]
    # exitcode
    exit_code = str(-99999)

    # check for entry
    if user_input is None:
        validate_pass = False
        return print(f'No input detected'), validate_pass

    # check for none integer input
    if not isinstance(user_input, int):
        validate_pass = False
        return print(f'{user_input} please enter integers only'), validate_pass

    # convert input to string
    input_to_string = str(user_input)

    if input_to_string == exit_code:
        return print(f'exit code')

    # check for input less than 4
    if len(input_to_string) <= 4:
        if len(input_to_string) < 4:
            return print(f'{input_to_string} has too few digits')

        if input_to_string[0] == '-':
            return print(f'{input_to_string} has too few digits')

    # check to make sure input is either length 5 if signed or 4 if unsigned
    if len(input_to_string) >= 5 and input_to_string != exit_code:
        if len(input_to_string) > 5:
            return print(f'{input_to_string} has too many digits')

        if len(input_to_string) == 5 and input_to_string[0] != '-':
            return print(f'{input_to_string} must be 4 digits only')

    # check if input is a negative value
    if input_to_string[0] == '-':
        if input_to_string != exit_code:
            # slice opcode as substring
            input_to_string = input_to_string[1:]
            operator = input_to_string[0:2]

            # check opcode
            if int(operator) not in opcodes:
                return print(f'{user_input} incorrect operator entered')

    input_operator = input_to_string[0:2]
    if int(input_operator) not in opcodes:
        return print(f'{user_input} incorrect operator entered')


def validate_memory(curr_mem_len):
    if curr_mem_len > 100:
        return print(f'Memory Exceeded')


def validate_instruct_counter(curr_counter_value):
    if curr_counter_value > 100:
        return print(f'Too many entries have been made')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    validate(-110)
    validate(-10)
    validate(-1)
    validate(110)
    validate(10)
    validate(1)
    validate(-11000)
    validate(11777)
    validate(1211)
    valid = validate('hello')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
