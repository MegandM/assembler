@0
D=M              // D = first number
@1
D=D-M            // D = first number - second number
@10
D;JGT            // if D>0 (first is greater) goto output_first
@1
D=M              // D = second number
@12
0;JMP            // goto output_d
@0
D=M              // D = first number
@2
M=D              // M[2] = D (greatest number)
@14
0;JMP            // infinite loop
