// push constant 17
@17
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 17
@17
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// eq
@SP
    AM=M-1
    D=M
    A=A-1
    D=M-D
    @TRUE_530507
    D;JEQ
    @SP
    A=M-1
    M=0
    @END_530507
    0;JMP
(TRUE_530507)
    @SP
    A=M-1
    M=-1
(END_530507)
// push constant 17
@17
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 16
@16
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// eq
@SP
    AM=M-1
    D=M
    A=A-1
    D=M-D
    @TRUE_263306
    D;JEQ
    @SP
    A=M-1
    M=0
    @END_263306
    0;JMP
(TRUE_263306)
    @SP
    A=M-1
    M=-1
(END_263306)
// push constant 16
@16
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 17
@17
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// eq
@SP
    AM=M-1
    D=M
    A=A-1
    D=M-D
    @TRUE_224670
    D;JEQ
    @SP
    A=M-1
    M=0
    @END_224670
    0;JMP
(TRUE_224670)
    @SP
    A=M-1
    M=-1
(END_224670)
// push constant 892
@892
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 891
@891
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// lt
@SP
    AM=M-1
    D=M
    A=A-1
    D=M-D
    @TRUE_653249
    D;JLT
    @SP
    A=M-1
    M=0
    @END_653249
    0;JMP
(TRUE_653249)
    @SP
    A=M-1
    M=-1
(END_653249)
// push constant 891
@891
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 892
@892
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// lt
@SP
    AM=M-1
    D=M
    A=A-1
    D=M-D
    @TRUE_350024
    D;JLT
    @SP
    A=M-1
    M=0
    @END_350024
    0;JMP
(TRUE_350024)
    @SP
    A=M-1
    M=-1
(END_350024)
// push constant 891
@891
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 891
@891
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// lt
@SP
    AM=M-1
    D=M
    A=A-1
    D=M-D
    @TRUE_704111
    D;JLT
    @SP
    A=M-1
    M=0
    @END_704111
    0;JMP
(TRUE_704111)
    @SP
    A=M-1
    M=-1
(END_704111)
// push constant 32767
@32767
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 32766
@32766
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// gt
@SP
    AM=M-1
    D=M
    A=A-1
    D=M-D
    @TRUE_868061
    D;JGT
    @SP
    A=M-1
    M=0
    @END_868061
    0;JMP
(TRUE_868061)
    @SP
    A=M-1
    M=-1
(END_868061)
// push constant 32766
@32766
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 32767
@32767
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// gt
@SP
    AM=M-1
    D=M
    A=A-1
    D=M-D
    @TRUE_957151
    D;JGT
    @SP
    A=M-1
    M=0
    @END_957151
    0;JMP
(TRUE_957151)
    @SP
    A=M-1
    M=-1
(END_957151)
// push constant 32766
@32766
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 32766
@32766
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// gt
@SP
    AM=M-1
    D=M
    A=A-1
    D=M-D
    @TRUE_643036
    D;JGT
    @SP
    A=M-1
    M=0
    @END_643036
    0;JMP
(TRUE_643036)
    @SP
    A=M-1
    M=-1
(END_643036)
// push constant 57
@57
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 31
@31
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// push constant 53
@53
    D=A
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
// push constant 112
@112
    D=A
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
// neg
@SP
    A=M-1
    M=-M
// and
@SP
    AM=M-1
    D=M
    A=A-1
    M=D&M
// push constant 82
@82
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
// or
@SP
    AM=M-1
    D=M
    A=A-1
    M=D|M
// not
@SP
    A=M-1
    M=!M

// Infinite loop at the end
(END)
    @END
    0;JMP
