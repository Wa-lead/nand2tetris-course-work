// push constant 3030
@3030
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// pop pointer 0
@3
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
// push constant 3040
@3040
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// pop pointer 1
@4
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
// push constant 32
@32
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// pop this 2
@THIS
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
// push constant 46
@46
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// pop that 6
@THAT
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
// push pointer 0
@3
    A=A
    D=M // Load value from RAM[A] into D
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push pointer 1
@4
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
// push this 2
@THIS
    D=M
    @2
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
// push that 6
@THAT
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

// Infinite loop at the end
(END)
    @END
    0;JMP
