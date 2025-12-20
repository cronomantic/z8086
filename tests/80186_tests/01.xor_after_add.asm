; 
; z8086 0.1 bug:
;   xor (0x31) fails after add (0x83) when the queue is full enough 
;
; RESULT 
; 10 00 20 00 18 00 00 00
; END_RESULT

use16

start:

mov sp, 0x10
mov ax, 0x20

mov [0], sp     ; 0x10
mov [2], ax     ; 0x20

mov bx, 1      
mul bx          ; fill prefetch queue

add sp, 8
xor ax, ax

mov [4], sp     ; 0x18
mov [6], ax     ; 0

hlt
