"""
tests for vm_translator.py
run: python3 example.py
"""

import os
import sys
import tempfile

from vm_translator import (
    get_command_parts,
    classify_command_type,
    write_arithmetic,
    write_push,
    write_pop,
    clean_line,
    parse_vm_file,
)

# need the assembler to do full pipeline tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'project06-assembler'))
from HackAssembler import first_pass_for_labels, second_pass_for_translation

PASS = 0
FAIL = 0

def check(name, got, expected):
    global PASS, FAIL
    if got == expected:
        PASS += 1
    else:
        FAIL += 1
        print(f"    FAIL {name}: got {got!r}, expected {expected!r}")


def test_get_command_parts():
    print("  get_command_parts")
    check("add",          get_command_parts('add'),                  ('add', None, None))
    check("push const 7", get_command_parts('push constant 7'),      ('push', 'constant', 7))
    check("pop local 0",  get_command_parts('pop local 0'),          ('pop', 'local', 0))
    check("pop temp 6",   get_command_parts('pop temp 6'),           ('pop', 'temp', 6))
    check("push static 1",get_command_parts('push static 1'),        ('push', 'static', 1))


def test_classify_command_type():
    print("  classify_command_type")
    for cmd in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
        check(f"{cmd}", classify_command_type(cmd), 'C_ARITHMETIC')
    check("push",     classify_command_type('push'),     'C_PUSH')
    check("pop",      classify_command_type('pop'),      'C_POP')
    check("label",    classify_command_type('label'),    'C_LABEL')
    check("goto",     classify_command_type('goto'),     'C_GOTO')
    check("if-goto",  classify_command_type('if-goto'),  'C_IF')
    check("function", classify_command_type('function'), 'C_FUNCTION')
    check("return",   classify_command_type('return'),   'C_RETURN')
    check("call",     classify_command_type('call'),     'C_CALL')

    # should blow up on garbage input
    try:
        classify_command_type('bogus')
        FAIL += 1
        print("    FAIL: 'bogus' should raise ValueError")
    except ValueError:
        global PASS
        PASS += 1


def test_clean_line():
    print("  clean_line")
    check("strip comment",   clean_line('push constant 7 // push 7'), 'push constant 7')
    check("only comment",    clean_line('// this is a comment'),       '')
    check("whitespace",      clean_line('  add  '),                    'add')
    check("empty",           clean_line(''),                           '')


def test_write_arithmetic():
    print("  write_arithmetic")

    # binary ops - check the key asm instruction is in there
    for op, expected_asm in [('add', 'M=D+M'), ('sub', 'M=M-D'), ('and', 'M=D&M'), ('or', 'M=D|M')]:
        asm = write_arithmetic(op)
        check(f"{op} has {expected_asm}", expected_asm in asm, True)
        check(f"{op} touches SP", '@SP' in asm, True)

    # unary
    asm = write_arithmetic('neg')
    check("neg has M=-M", 'M=-M' in asm, True)
    asm = write_arithmetic('not')
    check("not has M=!M", 'M=!M' in asm, True)

    # comparisons need labels + jump instructions
    for op, jmp in [('eq', 'JEQ'), ('gt', 'JGT'), ('lt', 'JLT')]:
        asm = write_arithmetic(op)
        check(f"{op} has {jmp}", jmp in asm, True)
        check(f"{op} has TRUE label", 'TRUE_' in asm, True)
        check(f"{op} has END label", 'END_' in asm, True)


def test_write_push():
    print("  write_push")

    asm = write_push('constant', 42, 'Test')
    check("push constant has @42", '@42' in asm, True)
    check("push constant has D=A", 'D=A' in asm, True)

    asm = write_push('local', 2, 'Test')
    check("push local has @LCL", '@LCL' in asm, True)
    check("push local has @2", '@2' in asm, True)

    # temp base is 5, so temp 3 -> @8
    asm = write_push('temp', 3, 'Test')
    check("push temp 3 has @8", '@8' in asm, True)

    # pointer 0 = THIS (addr 3), pointer 1 = THAT (addr 4)
    asm = write_push('pointer', 0, 'Test')
    check("push pointer 0 has @3", '@3' in asm, True)
    asm = write_push('pointer', 1, 'Test')
    check("push pointer 1 has @4", '@4' in asm, True)

    asm = write_push('static', 5, 'MyFile')
    check("push static has @MyFile.5", '@MyFile.5' in asm, True)


def test_write_pop():
    print("  write_pop")

    asm = write_pop('local', 0, 'Test')
    check("pop local has @LCL", '@LCL' in asm, True)
    check("pop local uses R13 as temp", '@R13' in asm, True)

    asm = write_pop('argument', 1, 'Test')
    check("pop argument has @ARG", '@ARG' in asm, True)

    asm = write_pop('temp', 2, 'Test')
    check("pop temp 2 has @7", '@7' in asm, True)

    asm = write_pop('static', 3, 'Foo')
    check("pop static has @Foo.3", '@Foo.3' in asm, True)


def test_translate_and_assemble():
    """translate every .vm -> .asm, then try to assemble it.
    if the assembler doesn't choke, the generated asm is at least syntactically valid."""
    print("  e2e: .vm -> .asm -> .hack")
    this_dir = os.path.dirname(__file__)
    vm_files = sorted(f for f in os.listdir(this_dir) if f.endswith('.vm'))

    for vm_file in vm_files:
        vm_path = os.path.join(this_dir, vm_file)
        with tempfile.NamedTemporaryFile(suffix='.asm', mode='w', delete=False) as tmp:
            tmp_asm = tmp.name

        try:
            parse_vm_file(vm_path, tmp_asm)

            with open(tmp_asm, 'r') as f:
                asm_lines = f.readlines()

            instructions, table = first_pass_for_labels(asm_lines)
            binary = second_pass_for_translation(instructions, table)

            global PASS
            PASS += 1
            print(f"    {vm_file:>20} -> {len(instructions):>4} asm -> {len(binary):>4} binary")
        except Exception as e:
            global FAIL
            FAIL += 1
            print(f"    FAIL {vm_file}: {e}")
        finally:
            os.unlink(tmp_asm)


# small cpu sim just for verifying the translated code actually works
class MiniCPU:
    COMP = {
        0b101010: lambda d, y: 0,      0b111111: lambda d, y: 1,
        0b111010: lambda d, y: -1,     0b001100: lambda d, y: d,
        0b110000: lambda d, y: y,      0b001101: lambda d, y: ~d,
        0b110001: lambda d, y: ~y,     0b001111: lambda d, y: -d,
        0b110011: lambda d, y: -y,     0b011111: lambda d, y: d + 1,
        0b110111: lambda d, y: y + 1,  0b001110: lambda d, y: d - 1,
        0b110010: lambda d, y: y - 1,  0b000010: lambda d, y: d + y,
        0b010011: lambda d, y: d - y,  0b000111: lambda d, y: y - d,
        0b000000: lambda d, y: d & y,  0b010101: lambda d, y: d | y,
    }

    def __init__(self):
        self.ram = [0] * 4096
        self.A = self.D = self.PC = 0

    def run(self, binary, max_steps=5000):
        rom = [int(line.strip(), 2) for line in binary if line.strip()]
        for _ in range(max_steps):
            if self.PC >= len(rom):
                break
            instr = rom[self.PC]
            if not (instr & 0x8000):
                self.A = instr & 0x7FFF
                self.PC += 1
            else:
                a = (instr >> 12) & 1
                comp = (instr >> 6) & 0x3F
                dest = (instr >> 3) & 7
                jump = instr & 7
                y = self.ram[self.A] if a else self.A
                result = self.COMP[comp](self.D, y) & 0xFFFF
                addr = self.A
                if dest & 1: self.ram[addr] = result
                if dest & 4: self.A = result
                if dest & 2: self.D = result
                s = result - 0x10000 if result >= 0x8000 else result
                jmp = ((jump >> 2) & 1 and s < 0) or ((jump >> 1) & 1 and s == 0) or (jump & 1 and s > 0)
                self.PC = addr if jmp else self.PC + 1
            # stop on infinite loop (end of program)
            if self.PC < len(rom) and rom[self.PC] & 0x8000 and (rom[self.PC] & 7) == 7:
                if self.A == self.PC:
                    break


def test_simpleadd_correctness():
    """the real test: translate SimpleAdd.vm, assemble it, run it on the cpu,
    and check that 7 + 8 = 15 ends up at the right place in RAM"""
    print("  cpu sim: SimpleAdd -> 7 + 8 = 15?")
    this_dir = os.path.dirname(__file__)
    vm_path = os.path.join(this_dir, 'SimpleAdd.vm')

    with tempfile.NamedTemporaryFile(suffix='.asm', mode='w', delete=False) as tmp:
        tmp_asm = tmp.name

    try:
        parse_vm_file(vm_path, tmp_asm)
        with open(tmp_asm, 'r') as f:
            asm_lines = f.readlines()

        instructions, table = first_pass_for_labels(asm_lines)
        binary = second_pass_for_translation(instructions, table)

        cpu = MiniCPU()
        cpu.ram[0] = 256  # SP starts at 256
        cpu.run(binary)

        sp = cpu.ram[0]
        result = cpu.ram[256]
        check("SP moved", sp > 256, True)
        check("7 + 8 = 15", result, 15)
        print(f"    SP={sp}, RAM[256]={result}")
    except Exception as e:
        global FAIL
        FAIL += 1
        print(f"    FAIL: {e}")
    finally:
        os.unlink(tmp_asm)


if __name__ == '__main__':
    print("=== project 7: vm translator tests ===\n")
    test_get_command_parts()
    test_classify_command_type()
    test_clean_line()
    test_write_arithmetic()
    test_write_push()
    test_write_pop()
    test_translate_and_assemble()
    test_simpleadd_correctness()
    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)
