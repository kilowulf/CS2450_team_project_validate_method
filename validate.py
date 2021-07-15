""" CS 2450 - Team Project:
    07-10-21
    Aaron Brown
        validate method:
                - test for None: no entry made
                - test for data types: int only
                - test for signed integer to extract operator code properly

"""


def validate(user_input):
    # Opcodes
    opcodes = [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43]

    # convert input to string
    input_to_string = str(user_input)

    # check if input is a negative value
    if input_to_string[0] == '-':
        input_to_string = input_to_string[1:3]
    operator = input_to_string[:2]

    # check for entry
    if user_input is None:
        print(f'No input detected')

    # check to make sure input is either length 5 if signed or 4 if unsigned
    if len(input_to_string) >= 5:
        if input_to_string[0] is not '-':
            print(f'input must be 4 digits only')

    # check for none integer input
    if not isinstance(user_input, int):
        print(f'{user_input} please enter integers only')
    # check opcode
    if int(operator) not in opcodes:
        print(f'{user_input} incorrect operator entered')


def validate_memory(curr_mem_len):
    if curr_mem_len > 100:
        print(f'Memory Exceeded')


def validate_instruct_counter(curr_counter_value):
    if curr_counter_value > 100:
        print(f'Too many entries have been made')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # test input for negative value
    user_input_value = -1011
    user_input_string = str(user_input_value)
    if user_input_string[0] == '-':
        user_input_string = user_input_string[1:3]

    # test input for valid opcode
    opcodes2 = [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43]
    if int(user_input_string) not in opcodes2:
        print(f'{user_input_string} is in opcodes')

    print(len(user_input_string))
    print(user_input_string[:2])

    # validate(user_input)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
