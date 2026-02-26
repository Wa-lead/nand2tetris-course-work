





// while true
//    if r2:
//       RAM[addr] = -1
//        addr = addr + 1
//    else:
//        RAM[addr] = 0
//        addr = addr -1


@SCREEN
D=A 
@addr
M=D

@8192
D=D+A
@SCREEN_LIMIT
M=D

(LOOP_WHITE)
    @KBD
    D=M
    @LOOP_BLACK
    D;JNE

    @addr
    D=M

    // if address == screen (beginning of the screen then just go back)
    @SCREEN
    D=D-A
    @LOOP_WHITE
    D;JEQ


    @addr
    A=M
    M=0

    @addr
    M=M-1

    @LOOP_WHITE
    0;JMP



(LOOP_BLACK)
    @KBD
    D=M
    @LOOP_WHITE
    D;JEQ


    @addr
    D=M

    @SCREEN_LIMIT
    D=D-M
    @LOOP_BLACK
    D;JGT
   


    @addr
    A=M
    M=-1

    @addr
    M=M+1

    @LOOP_BLACK
    0;JMP
