"""
tests for HackAssembler.py
run: python3 example.py
"""

import os
import sys

from HackAssembler import (
    initialize_symbol_table,
    classify_instruction,
    parse_a_instruction,
    parse_c_instruction,
    translate_a_instruction,
    translate_c_instruction,
    first_pass_for_labels,
    second_pass_for_translation,
)

PASS = 0
FAIL = 0

def check(name, got, expected):
    global PASS, FAIL
    if got == expected:
        PASS += 1
    else:
        FAIL += 1
        print(f"    FAIL {name}: got {got!r}, expected {expected!r}")


def test_symbol_table():
    print("  symbol table init")
    table = initialize_symbol_table()
    check("SP",     table['SP'],     0)
    check("LCL",    table['LCL'],    1)
    check("ARG",    table['ARG'],    2)
    check("THIS",   table['THIS'],   3)
    check("THAT",   table['THAT'],   4)
    check("R0",     table['R0'],     0)
    check("R15",    table['R15'],    15)
    check("SCREEN", table['SCREEN'], 16384)
    check("KBD",    table['KBD'],    24576)


def test_classify():
    print("  classify_instruction")
    check("A-instr",  classify_instruction('@100'),      'A_INSTRUCTION')
    check("A-symbol", classify_instruction('@LOOP'),     'A_INSTRUCTION')
    check("L-cmd",    classify_instruction('(LOOP)'),    'L_COMMAND')
    check("C-instr",  classify_instruction('D=A'),       'C_INSTRUCTION')
    check("C-jump",   classify_instruction('0;JMP'),     'C_INSTRUCTION')
    check("C-full",   classify_instruction('D=D+A;JGT'), 'C_INSTRUCTION')


def test_parse_a():
    print("  parse_a_instruction")
    check("numeric", parse_a_instruction('@100'),  '100')
    check("symbol",  parse_a_instruction('@LOOP'), 'LOOP')
    check("R0",      parse_a_instruction('@R0'),   'R0')


def test_parse_c():
    print("  parse_c_instruction")

    r = parse_c_instruction('D=A')
    check("D=A dest", r['dest'], 'D')
    check("D=A comp", r['comp'], 'A')
    check("D=A jump", r['jump'], 'null')

    r = parse_c_instruction('0;JMP')
    check("0;JMP dest", r['dest'], 'null')
    check("0;JMP comp", r['comp'], '0')
    check("0;JMP jump", r['jump'], 'JMP')

    r = parse_c_instruction('D=D+A;JGT')
    check("D=D+A;JGT dest", r['dest'], 'D')
    check("D=D+A;JGT comp", r['comp'], 'D+A')
    check("D=D+A;JGT jump", r['jump'], 'JGT')

    r = parse_c_instruction('AM=M-1')
    check("AM=M-1 dest", r['dest'], 'AM')
    check("AM=M-1 comp", r['comp'], 'M-1')

    r = parse_c_instruction('D;JEQ')
    check("D;JEQ dest", r['dest'], 'null')
    check("D;JEQ comp", r['comp'], 'D')
    check("D;JEQ jump", r['jump'], 'JEQ')


def test_translate_a():
    print("  translate_a_instruction")
    table = initialize_symbol_table()

    binary, cnt = translate_a_instruction('0', table, 16)
    check("@0", binary, '0' + '0' * 15)

    binary, cnt = translate_a_instruction('100', table, 16)
    check("@100", binary, f'0{100:015b}')

    # predefined symbols
    binary, cnt = translate_a_instruction('SP', table, 16)
    check("@SP -> 0", binary, '0' + '0' * 15)

    binary, cnt = translate_a_instruction('SCREEN', table, 16)
    check("@SCREEN -> 16384", binary, f'0{16384:015b}')

    # new var should get allocated at RAM[16]
    binary, cnt = translate_a_instruction('myVar', table, 16)
    check("@myVar addr", binary, f'0{16:015b}')
    check("@myVar counter", cnt, 17)

    # same var again should reuse the address
    binary, cnt = translate_a_instruction('myVar', table, 17)
    check("@myVar reuse", binary, f'0{16:015b}')
    check("@myVar counter unchanged", cnt, 17)


def test_translate_c():
    print("  translate_c_instruction")

    # format: 111 + comp(7bits) + dest(3bits) + jump(3bits)
    r = translate_c_instruction({'dest': 'D', 'comp': 'A', 'jump': 'null'})
    check("D=A", r, '111' + '0110000' + '010' + '000')

    r = translate_c_instruction({'dest': 'null', 'comp': '0', 'jump': 'JMP'})
    check("0;JMP", r, '111' + '0101010' + '000' + '111')

    r = translate_c_instruction({'dest': 'M', 'comp': 'D+M', 'jump': 'null'})
    check("M=D+M", r, '111' + '1000010' + '001' + '000')

    r = translate_c_instruction({'dest': 'AMD', 'comp': 'D+1', 'jump': 'null'})
    check("AMD=D+1", r, '111' + '0011111' + '111' + '000')


def test_first_pass():
    print("  first_pass_for_labels")
    program = [
        '// comment\n',
        '@R0\n',
        'D=M\n',
        '(LOOP)\n',
        '  D=D-1  // decrement\n',
        '@LOOP\n',
        'D;JGT\n',
        '(END)\n',
        '@END\n',
        '0;JMP\n',
    ]
    instructions, table = first_pass_for_labels(program)

    check("instruction count", len(instructions), 7)  # labels don't count
    check("LOOP label addr",   table['LOOP'], 2)
    check("END label addr",    table['END'], 5)
    check("no label in code",  '(LOOP)' not in instructions, True)


def test_assemble_mult():
    """assemble Mult.asm and compare against the reference .hack file"""
    print("  e2e: Mult.asm vs Mult.hack")
    mult_asm = os.path.join(os.path.dirname(__file__), '..', 'project04-machine-language', 'Mult.asm')
    mult_hack = os.path.join(os.path.dirname(__file__), 'Mult.hack')

    if not os.path.exists(mult_asm):
        print("    SKIP: Mult.asm not found")
        return
    if not os.path.exists(mult_hack):
        print("    SKIP: Mult.hack reference not found")
        return

    with open(mult_asm, 'r') as f:
        lines = f.readlines()

    instructions, table = first_pass_for_labels(lines)
    binary = second_pass_for_translation(instructions, table)

    with open(mult_hack, 'r') as f:
        expected = [line.strip() for line in f if line.strip()]

    check("line count matches", len(binary), len(expected))

    mismatches = 0
    for i, (got, exp) in enumerate(zip(binary, expected)):
        if got != exp:
            mismatches += 1
            if mismatches <= 3:
                print(f"    line {i}: got {got}, expected {exp}")

    if mismatches == 0:
        print(f"    all {len(binary)} lines match reference")
    else:
        global FAIL
        FAIL += 1
        print(f"    {mismatches} mismatched lines")


def test_assemble_rect():
    """just make sure Rect.asm assembles without blowing up"""
    print("  e2e: Rect.asm (smoke test)")
    rect_asm = os.path.join(os.path.dirname(__file__), 'Rect.asm')
    if not os.path.exists(rect_asm):
        print("    SKIP: Rect.asm not found")
        return

    with open(rect_asm, 'r') as f:
        lines = f.readlines()

    instructions, table = first_pass_for_labels(lines)
    binary = second_pass_for_translation(instructions, table)
    check("Rect produces binary", len(binary) > 0, True)
    print(f"    assembled {len(binary)} instructions")


if __name__ == '__main__':
    print("=== project 6: assembler tests ===\n")
    test_symbol_table()
    test_classify()
    test_parse_a()
    test_parse_c()
    test_translate_a()
    test_translate_c()
    test_first_pass()
    test_assemble_mult()
    test_assemble_rect()
    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)
