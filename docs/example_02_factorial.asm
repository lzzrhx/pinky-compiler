; Motorola 68K example
; Calculate the factorial of 5

Num: DC.W 5
Res: DC.W 1

FACTORIAL:
    MOVE Num, D0  ; Num = 5
    MOVE Res, D1  ; Res = 1
LOOP:
    CMP #1, D0    ; Compare D0==1
    BEQ END
    MULS D0, D1   ; res = res * num
    SUB #1, D0    ; n--
    JMP LOOP
END:
    MOVE D1, Res

