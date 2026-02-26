# nand2tetris

my work through the [nand2tetris](https://www.nand2tetris.org/) course — building a computer from scratch, starting from NAND gates all the way up to a compiler.

based on the book "The Elements of Computing Systems" by Noam Nisan and Shimon Schocken.

## projects

| folder | project | what's in it |
|--------|---------|-------------|
| `project01-boolean-logic/` | boolean logic | 15 HDL chips built from NAND (Not, And, Or, Mux, DMux, etc.) |
| `project02-boolean-arithmetic/` | boolean arithmetic | HalfAdder, FullAdder, Add16, Inc16, ALU |
| `project03-sequential-logic/` | sequential logic | Bit, Register, RAM (8 to 16K), PC |
| `project04-machine-language/` | machine language | hand-written Hack assembly — Mult.asm, Fill.asm |
| `project05-computer-architecture/` | computer architecture | CPU, Memory, and Computer in HDL |
| `project06-assembler/` | assembler | Hack assembler in python (`.asm` → `.hack`) |
| `project07-vm-stack-arithmetic/` | VM I: stack arithmetic | VM translator in python (`.vm` → `.asm`) |
| `project08-vm-program-control/` | VM II: program control | function calls, loops, branching — test programs |
| `project09-high-level-language/` | high-level language | two Jack programs: a 3D cube renderer and a bloxors puzzle game |
| `project10-compiler-syntax-analysis/` | compiler I: syntax analysis | Jack tokenizer + recursive descent parser in python |

## testing

projects 6, 7, and 10 have `example.py` test scripts:

```bash
cd project06-assembler && python3 example.py
cd project07-vm-stack-arithmetic && python3 example.py
cd project10-compiler-syntax-analysis && python3 example.py
```

## progress

completed through project 10. projects 11 (code generation) and 12 (OS) are still on the list.
