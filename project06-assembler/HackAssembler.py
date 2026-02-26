import sys

# --- Part 1: Constants and Translation Maps ---
# These maps are the "knowledge base" for C-instruction translation.
COMP_MAP = {
    '0':   '0101010', '1':   '0111111', '-1':  '0111010', 'D':   '0001100',
    'A':   '0110000', '!D':  '0001101', '!A':  '0110001', '-D':  '0001111',
    '-A':  '0110011', 'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
    'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111',
    'D&A': '0000000', 'D|A': '0010101', 'M':   '1110000', '!M':  '1110001',
    '-M':  '1110011', 'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010',
    'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000', 'D|M': '1010101'
}
DEST_MAP = {'null':'000', 'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'}
JUMP_MAP = {'null':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}

# --- Part 2: Symbol Table Management ---
def initialize_symbol_table():
    """Creates the symbol table and fills it with predefined symbols."""
    table = { 'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 'SCREEN': 16384, 'KBD': 24576 }
    for i in range(16):
        table[f'R{i}'] = i
    return table

# --- Part 3: Classification and Parsing Functions ---
def classify_instruction(line):
    """Determines the type of a clean instruction line."""
    if line.startswith('@'): return 'A_INSTRUCTION'
    if line.startswith('('): return 'L_COMMAND'
    return 'C_INSTRUCTION'

def parse_a_instruction(line):
    """Extracts the symbol or value from an A-instruction."""
    return line[1:]

def parse_c_instruction(line):
    """Parses a C-instruction into its 'dest', 'comp', and 'jump' parts."""
    dest, comp, jump = 'null', '', 'null'
    if '=' in line:
        dest, line = line.split('=', 1)
    if ';' in line:
        comp, jump = line.split(';', 1)
    else:
        comp = line
    return {'dest': dest, 'comp': comp, 'jump': jump}

# --- Part 4: Translation Functions ---
def translate_a_instruction(symbol, symbol_table, ram_address_counter):
    """Translates a parsed A-instruction into binary."""
    if symbol.isdigit():
        address = int(symbol)
    else:
        if symbol not in symbol_table:
            symbol_table[symbol] = ram_address_counter
            ram_address_counter += 1
        address = symbol_table[symbol]
    return f'0{address:015b}', ram_address_counter

def translate_c_instruction(parts):
    """Translates parsed C-instruction parts into binary."""
    comp_bits = COMP_MAP[parts['comp']]
    dest_bits = DEST_MAP[parts['dest']]
    jump_bits = JUMP_MAP[parts['jump']]
    return f'111{comp_bits}{dest_bits}{jump_bits}'

# --- Part 5: The Two Passes ---
def first_pass_for_labels(lines):
    """
    Builds the symbol table for labels and returns a list of clean instructions.
    """
    symbol_table = initialize_symbol_table()
    clean_instructions = []
    rom_address = 0
    for line in lines:
        clean_line = line.split('//')[0].strip()
        if not clean_line:
            continue
        
        instr_type = classify_instruction(clean_line)
        if instr_type == 'L_COMMAND':
            symbol_table[clean_line[1:-1]] = rom_address
        else:
            clean_instructions.append(clean_line)
            rom_address += 1
            
    return clean_instructions, symbol_table

def second_pass_for_translation(instructions, symbol_table):
    """
    Translates a clean list of instructions into binary code.
    """
    binary_code = []
    next_ram_address = 16 # Variables are allocated from RAM address 16
    
    for instruction in instructions:
        instr_type = classify_instruction(instruction)
        
        if instr_type == 'A_INSTRUCTION':
            symbol = parse_a_instruction(instruction)
            binary_line, next_ram_address = translate_a_instruction(symbol, symbol_table, next_ram_address)
            binary_code.append(binary_line)
            
        elif instr_type == 'C_INSTRUCTION':
            parts = parse_c_instruction(instruction)
            binary_line = translate_c_instruction(parts)
            binary_code.append(binary_line)
            
    return binary_code

# --- Part 6: Main Orchestrator ---
def assemble(input_file):
    """Orchestrates the two-pass assembly process."""
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    # Pass 1: Handle labels and clean the code
    instructions, symbol_table = first_pass_for_labels(lines)
    
    # Pass 2: Translate instructions to binary
    binary_code = second_pass_for_translation(instructions, symbol_table)

    # Write the output
    output_file = input_file.replace('.asm', '.hack')
    with open(output_file, 'w') as f:
        f.write('\n'.join(binary_code))
        f.write('\n')
        
    print(f"Assembly successful. Output written to {output_file}")



if __name__ == '__main__':
    assemble(input_file='nand2tetris/SimpleAdd.asm')