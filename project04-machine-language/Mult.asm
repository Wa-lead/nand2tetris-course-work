

// while(i<r1):
//      r2 = r2 + r0
//      i = i + 1
    



@i 
M=0

(LOOP)
    // condition check
    @i
    D=M

    @R1
    D=D-M

    @END
    D;JEQ


    //logic
    @R0
    D=M

    @R2
    M=D+M

    @i 
    M=M+1


    @LOOP
    0;JMP

(END)

    @END
    0;JMP



// NOTE: you can make this faster via making it looping MIN(r1,r2) times.