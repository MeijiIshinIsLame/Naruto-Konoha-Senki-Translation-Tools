.gba
.open "{source}","{dest}",0x08000000 

//============== HOOK ======================
.org 0x08066274
	bl namelabel_check

.org 0x0809e700
namelabel_check:
	;check if in range of charnames
	push {r6, r7}
	ldr r6, =lower_addr
	ldr r6, [r6]
	ldr r7, =higher_addr
	ldr r7, [r7]
	cmp r1, r7
	bge finale ;get outta here!
	cmp r1, r6
	bge subvert_nametable
finale:
	; instructions we wrote over
	pop {r6, r7}
	sub sp, #0x24
	add r6, r0, 0h
	; end instructions we wrote over
	bx lr
subvert_nametable:
	ldr r1, [r1]
	b finale
	;we want to jump to my personal table with 2byte SJIS eng chars

.pool
lower_addr:
	.word 0x085a57d0

higher_addr:
	.word 0x085a632f

.close
