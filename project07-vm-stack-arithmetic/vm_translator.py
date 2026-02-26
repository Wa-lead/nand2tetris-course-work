import random
import os

def get_command_parts(line):
    """Extracts the command and its arguments from a line of VM code."""
    parts = line.split()
    command = parts[0]
    arg1 = parts[1] if len(parts) > 1 else None
    arg2 = int(parts[2]) if len(parts) > 2 else None
    return command, arg1, arg2

def classify_command_type(command):
    """Classifies the command into its C-Type."""
    ARITHMETIC_COMMANDS = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
    if command in ARITHMETIC_COMMANDS:
        return 'C_ARITHMETIC'
    
    COMMAND_MAP = {
        'push': 'C_PUSH', 'pop': 'C_POP', 'label': 'C_LABEL',
        'goto': 'C_GOTO', 'if-goto': 'C_IF', 'function': 'C_FUNCTION',
        'return': 'C_RETURN', 'call': 'C_CALL'
    }
    
    c_type = COMMAND_MAP.get(command)
    if not c_type:
        raise ValueError(f"Unknown command type: {command}")
    return c_type

def write_arithmetic(command):
    """Generates assembly code for an arithmetic command."""
    if command in ['add', 'sub', 'and', 'or']:
        return _write_binary_op(command)
    elif command in ['neg', 'not']:
        return _write_unary_op(command)
    elif command in ['eq', 'gt', 'lt']:
        return _write_comparison_op(command)

def _write_binary_op(command):
    """Handles add, sub, and, or."""
    op_map = {'add': 'M=D+M', 'sub': 'M=M-D', 'and': 'M=D&M', 'or': 'M=D|M'}
    return f"""
    @SP
    AM=M-1
    D=M
    A=A-1
    {op_map[command]}
"""

def _write_unary_op(command):
    """Handles neg, not."""
    op_map = {'neg': 'M=-M', 'not': 'M=!M'}
    return f"""
    @SP
    A=M-1
    {op_map[command]}
"""

def _write_comparison_op(command):
    """Handles eq, gt, lt."""
    jump_map = {'eq': 'JEQ', 'gt': 'JGT', 'lt': 'JLT'}
    label_suffix = random.randint(1, 999999)
    return f"""
    @SP
    AM=M-1
    D=M
    A=A-1
    D=M-D
    @TRUE_{label_suffix}
    D;{jump_map[command]}
    @SP
    A=M-1
    M=0
    @END_{label_suffix}
    0;JMP
(TRUE_{label_suffix})
    @SP
    A=M-1
    M=-1
(END_{label_suffix})
"""

def _get_address_calc(segment, index, static_filename):
    """Helper to generate assembly for calculating an effective memory address and
       placing it into the A register."""
    if segment in ['local', 'argument', 'this', 'that']:
        segment_map = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
        return f"""
    @{segment_map[segment]}
    D=M
    @{index}
    A=D+A""" # A now holds the final address
    elif segment == 'temp':
        return f"""
    @{5 + index}
    A=A""" # A now holds the final address (e.g., @5, A=A)
    elif segment == 'pointer':
        return f"""
    @{3 + index}
    A=A""" # A now holds the final address (e.g., @3, A=A)
    elif segment == 'static':
        return f"""
    @{static_filename}.{index}
    A=A""" # A now holds the final address
    raise ValueError(f"Unknown segment: {segment}")

def write_push(segment, index, static_filename):
    """Generates assembly code for a push operation."""
    if segment == 'constant':
        return f"""
    @{index}
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
"""
    
    # Calculate the address and put it into A
    address_calc_asm = _get_address_calc(segment, index, static_filename)
    
    # Common code: load value from A into D, then push D to stack
    return address_calc_asm + """
    D=M // Load value from RAM[A] into D
    @SP
    A=M
    M=D
    @SP
    M=M+1
"""

def write_pop(segment, index, static_filename):
    """Generates assembly code for a pop operation."""
    # Calculate the address and put it into A
    address_calc_asm = _get_address_calc(segment, index, static_filename)

    # Common code: store the target address (from A) into R13,
    # then pop value from stack into D, then store D into RAM[R13]
    return address_calc_asm + f"""
    D=A // the index of the popped value
    @R13 // the index of the popped value
    M=D 
    @SP // the stack pointer
    AM=M-1 // the value of the stack pointer
    D=M // the value at the stack pointer
    @R13 // the index of the popped value
    A=M 
    M=D // 
"""


def clean_line(line):
    """Removes comments and leading/trailing whitespace."""
    return line.split('//')[0].strip()

def add_end_loop():
    """Generates an infinite loop at the end of the assembly file."""
    return """
// Infinite loop at the end
(END)
    @END
    0;JMP
"""

def parse_vm_file(input_file, output_file):
    """Translates a .vm file into a .asm file."""
    static_filename = os.path.basename(output_file).split('.')[0]

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            cleaned_line = clean_line(line)
            if not cleaned_line:
                continue

            command, arg1, arg2 = get_command_parts(cleaned_line)
            c_type = classify_command_type(command)
            assembly_code = ""

            if c_type == 'C_ARITHMETIC':
                assembly_code = write_arithmetic(command)
            elif c_type == 'C_PUSH':
                assembly_code = write_push(arg1, arg2, static_filename)
            elif c_type == 'C_POP':
                assembly_code = write_pop(arg1, arg2, static_filename)
            outfile.write(f"// {cleaned_line}\n{assembly_code.strip()}\n")
            
        outfile.write(add_end_loop())


if __name__ == '__main__':
    parse_vm_file('StaticTest.vm', 'StaticTest.asm')