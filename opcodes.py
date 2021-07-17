
import math

""" CS 2450 - Team Project:
    07-16-21
    Aaron Brown
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

                ** Arguments are assumed to be full 4 digit opcodes when passed to parameters as ie. src_add
                   dest_add, opcode.
                   
        Instruction register(IR):
                - pointer to follow current opcode (instruction code)/ mem location
                - contains actual instruction read from memory
                
        Instruction counter(PC - Program counter):
                - holds address of next instruction to be executed
                - upon fetching instruction; counter is incremented by single address value
                - contains address of the instruction to be executed
                
                ** may need clarification on exact roles from professor            
                   
                ** instruction counter will have to be incremented with each opcode input
                ** instruction register refers to current memory location

"""

"global variable"
accumulator = 0


def mem_add_locator(opcode):
    """extracts mem loc. from opcode and returns 2 digit integer"""
    op_str = str(opcode)
    if opcode is not None:
        mem_loc = op_str[2:]
        if mem_loc[0] == 0:
            mem_loc = op_str[3:]
        return int(mem_loc)
    else:
        pass
        'halt()'


def read(dest_add, memory_struct, word):
    "READ operation"
    mem_loc = mem_add_locator(dest_add)
    memory_struct[mem_loc] = word
    return print(f'READ from {mem_loc}: {memory_struct[mem_loc]}')


def write(src_add, memory_struct):
    "WRITE operation"
    mem_loc = mem_add_locator(src_add)
    return print(f'WRITE from {mem_loc}: {memory_struct[mem_loc]}')


def load(src_add, memory_struct):
    "LOAD operation"
    mem_loc = mem_add_locator(src_add)
    value_to_load = memory_struct[mem_loc]
    global accumulator
    accumulator = value_to_load
    return print(f'LOAD from {mem_loc} to Accumulator {accumulator}')


def store(dest_add, mem_struct, accum):
    "STORE operation"
    value_to_store = accum
    mem_loc = mem_add_locator(dest_add)
    mem_struct[mem_loc] = value_to_store
    return print(f'STORE {value_to_store} from accumulator to memory loc.: {mem_loc}')


def add(src_add, mem_struct):
    "ADD operation"
    mem_loc = mem_add_locator(src_add)
    value_to_add = mem_struct[mem_loc]
    global accumulator
    accumulator += value_to_add
    return print(f'ADD {value_to_add} at mem loc. {mem_loc} to accumulator: {accumulator}')


def subtract(src_add, mem_struct):
    "SUBTRACT operation"
    mem_loc = mem_add_locator(src_add)
    value_to_sub = mem_struct[mem_loc]
    global accumulator
    accumulator -= value_to_sub
    return print(f'SUBTRACT {value_to_sub} at mem loc. {mem_loc} from accumulator: {accumulator}')


def divide(src_add, mem_struct):
    """DIVIDE operation:
        may need to check numerator doesnt exceed size of denominator/accumulator value
        - what is expected behavior if result is float?
        - ceiling or floor operation?

    """
    mem_loc = mem_add_locator(src_add)
    value_denominator = mem_struct[mem_loc]
    global accumulator
    accumulator /= value_denominator

    return print(f'DIVIDE {value_denominator} at mem loc. {mem_loc} from accumulator: {int(accumulator)}')


def multiply(src_add, mem_struct):
    "MULTIPLY operation"
    mem_loc = mem_add_locator(src_add)
    value_to_multi = mem_struct[mem_loc]
    global accumulator
    accumulator *= value_to_multi
    return print(f'MULTIPLY {value_to_multi} at mem loc. {mem_loc} to accumulator: {int(accumulator)}')


def branch(br_add, mem_struct):
    """BRANCH operation:
            - move instruction register to branch mem loc.
    """
    mem_loc = mem_add_locator(br_add)
    branch_to_add = mem_struct[mem_loc]
    return print(f'BRANCH to mem loc. {mem_loc} with value: {branch_to_add} ')


def branch_neg(br_add, mem_struct):
    """BRANCHNEG operation:
            - if value in accumulator is negative: Branch to mem loc.
    """
    mem_loc = mem_add_locator(br_add)
    branch_to_add = mem_struct[mem_loc]
    global accumulator
    if accumulator < 0:
        return print(f'BRANCHNEG to mem loc. {mem_loc} with value: {branch_to_add}')


def halt():
    """HALT operation:
        - suspend / pause operations until a interrupt or reset is received
        - not sure how this works without a reset or interrupt operator; ask professor

    """
    pass


if __name__ == '__main__':

    memory = [None] * 100
    memory[2] = 1
    memory[99] = 15
    memory[97] = 34
    opcode_ex = 1210

    "should return last two digits of opcode as a memory location"
    print(mem_add_locator(opcode_ex))

    "should read a value into memory location"
    read(1098, memory, 23)

    "should return to console a value located at mem loc. "
    write(1199, memory)

    "load value from mem loc. to accumulator"
    load(2099, memory)

    "Store a value from accumulator to mem loc."
    store(2196, memory, accumulator)
    write(1196, memory)

    "Add a value located at mem loc to value in accumulator; result kept in accumulator"
    add(3098, memory)

    "subtract value at mem loc. from value in accumulator; result kept in accumulator"
    subtract(3197, memory)

    "Divide a value at mem loc. from value in accumulator; result kept in accumulator"
    divide(3202, memory)

    "Multiply a value at mem loc. to a  value in accumulator; result kept in accumulator"
    multiply(3399, memory)

    "Branch to mem loc. "
    branch(4067, memory)

    "Branch to mem loc. if value in accumulator is Negative value"
    read(1045, memory, -12)
    load(2045, memory)
    branch_neg(4267, memory)





