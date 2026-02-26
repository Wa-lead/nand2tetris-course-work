// push constant 10
@10
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// pop local 0
@LCL
    D=M
    @0
    A=D+A
    D=A // D now holds the target address (RAM[A])
    @R13
    M=D // R13 = target_address
    @SP
    AM=M-1 // SP--, A = new SP
    D=M // D = value popped from stack
    @R13
    A=M // A = target_address
    M=D // RAM[target_address] = popped_value
// push constant 21
@21
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 22
@22
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// pop argument 2
@ARG
    D=M
    @2
    A=D+A
    D=A // D now holds the target address (RAM[A])
    @R13
    M=D // R13 = target_address
    @SP
    AM=M-1 // SP--, A = new SP
    D=M // D = value popped from stack
    @R13
    A=M // A = target_address
    M=D // RAM[target_address] = popped_value
// pop argument 1
@ARG
    D=M
    @1
    A=D+A
    D=A // D now holds the target address (RAM[A])
    @R13
    M=D // R13 = target_address
    @SP
    AM=M-1 // SP--, A = new SP
    D=M // D = value popped from stack
    @R13
    A=M // A = target_address
    M=D // RAM[target_address] = popped_value
// push constant 36
@36
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// pop this 6
@THIS
    D=M
    @6
    A=D+A
    D=A // D now holds the target address (RAM[A])
    @R13
    M=D // R13 = target_address
    @SP
    AM=M-1 // SP--, A = new SP
    D=M // D = value popped from stack
    @R13
    A=M // A = target_address
    M=D // RAM[target_address] = popped_value
// push constant 42
@42
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 45
@45
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// pop that 5
@THAT
    D=M
    @5
    A=D+A
    D=A // D now holds the target address (RAM[A])
    @R13
    M=D // R13 = target_address
    @SP
    AM=M-1 // SP--, A = new SP
    D=M // D = value popped from stack
    @R13
    A=M // A = target_address
    M=D // RAM[target_address] = popped_value
// pop that 2
@THAT
    D=M
    @2
    A=D+A
    D=A // D now holds the target address (RAM[A])
    @R13
    M=D // R13 = target_address
    @SP
    AM=M-1 // SP--, A = new SP
    D=M // D = value popped from stack
    @R13
    A=M // A = target_address
    M=D // RAM[target_address] = popped_value
// push constant 510
@510
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// pop temp 6
@11
    A=A
    D=A // D now holds the target address (RAM[A])
    @R13
    M=D // R13 = target_address
    @SP
    AM=M-1 // SP--, A = new SP
    D=M // D = value popped from stack
    @R13
    A=M // A = target_address
    M=D // RAM[target_address] = popped_value
// push local 0
@LCL
    D=M
    @0
    A=D+A
    D=M // Load value from RAM[A] into D
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push that 5
@THAT
    D=M
    @5
    A=D+A
    D=M // Load value from RAM[A] into D
    @SP
    A=M
    M=D
    @SP
    M=M+1
// add
@SP
    AM=M-1
    D=M
    A=A-1
    M=D+M
// push argument 1
@ARG
    D=M
    @1
    A=D+A
    D=M // Load value from RAM[A] into D
    @SP
    A=M
    M=D
    @SP
    M=M+1
// sub
@SP
    AM=M-1
    D=M
    A=A-1
    M=M-D
// push this 6
@THIS
    D=M
    @6
    A=D+A
    D=M // Load value from RAM[A] into D
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push this 6
@THIS
    D=M
    @6
    A=D+A
    D=M // Load value from RAM[A] into D
    @SP
    A=M
    M=D
    @SP
    M=M+1
// add
@SP
    AM=M-1
    D=M
    A=A-1
    M=D+M
// sub
@SP
    AM=M-1
    D=M
    A=A-1
    M=M-D
// push temp 6
@11
    A=A
    D=M // Load value from RAM[A] into D
    @SP
    A=M
    M=D
    @SP
    M=M+1
// add
@SP
    AM=M-1
    D=M
    A=A-1
    M=D+M

// Infinite loop at the end
(END)
    @END
    0;JMP
